import json
import os
import re
from typing import List, Tuple
from app.models import Product

class RetrievalService:
    def __init__(self):
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")
        with open(data_path, "r") as f:
            products_data = json.load(f)
            self.products = [Product(**p) for p in products_data]
            
        # Common stop words to refine search intent
        self.stop_words = {"the", "and", "for", "with", "show", "give", "me", "what", "is", "are", "i", "need", "looking", "about", "want"}

    def get_all_products(self, category: str = None) -> List[Product]:
        if category:
            return [p for p in self.products if p.category.lower() == category.lower()]
        return self.products

    def retrieve_top_products(self, query: str, top_n: int = 3) -> List[Product]:
        """
        Retrieves products based on keyword matching across multiple fields.
        Scores: Category (10), Name (5), Tags (5), Description (2)
        """
        query_lower = query.lower()
        # Extract alphanumeric words
        search_terms = re.findall(r'\w+', query_lower)
        search_terms = [w for w in search_terms if w not in self.stop_words]

        # Detect price constraints (e.g., "under 1000")
        price_limit = None
        price_match = re.search(r'(?:under|less than|below|budget|max|maximum)\s*(\d+)', query_lower)
        if price_match:
            price_limit = float(price_match.group(1))

        scored_products: List[Tuple[float, Product]] = []

        for product in self.products:
            # Strict price filter if requested
            if price_limit and product.price > price_limit:
                continue

            score = 0
            p_cat = product.category.lower()
            p_name = product.name.lower()
            p_desc = product.description.lower()
            p_tags = [t.lower() for t in product.tags]

            for term in search_terms:
                if term.isdigit(): continue
                
                # Check Category
                if term == p_cat or term.rstrip('s') == p_cat.rstrip('s'):
                    score += 10
                
                # Check Name and Tags
                if term in p_name: score += 5
                if any(term == t for t in p_tags): score += 5
                
                # Check Description
                if term in p_desc: score += 2

            if score > 0:
                scored_products.append((score, product))

        # Sort by score descending and take top N
        scored_products.sort(key=lambda x: x[0], reverse=True)
        return [p for score, p in scored_products[:top_n]]

retrieval_service = RetrievalService()
