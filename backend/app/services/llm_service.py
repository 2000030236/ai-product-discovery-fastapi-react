import httpx
import json
import logging
from typing import List
from app.config import settings
from app.models import Product, LLMRecommendation

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def get_recommendations(self, query: str, products: List[Product]) -> LLMRecommendation:
        """
        Sends retrieved products to LLM for final recommendation and summarization.
        Ensures strict JSON output and handles parsing errors.
        """
        if not products:
            return LLMRecommendation(
                productIds=[],
                summary="We don't have this item. But we recommend these top rated items as alternatives below."
            )

        products_context = json.dumps([p.dict() for p in products], indent=1)
        
        prompt = f"""
You are a product recommendation assistant.
User Query: "{query}"

Retrieved Products:
{products_context}

Your Tasks:
1. Filter the products based on the query (intent, category, price).
2. If the user's specific request isn't found, explain that we don't have it and suggest the best alternatives from the list.
3. Return STRICTLY valid JSON according to the schema below.
4. Do not include any explanations or chatter outside the JSON.

SCHEMA:
{{
  "productIds": [number],
  "summary": "string"
}}
"""

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Ollama error: {response.status_code}")
                    raise Exception("AI service failed to respond")

                result = response.json()
                response_text = result.get("response", "").strip()
                
                try:
                    data = json.loads(response_text)
                    return LLMRecommendation(
                        productIds=data.get("productIds", []),
                        summary=data.get("summary", "I've picked these options for you.")
                    )
                except (json.JSONDecodeError, KeyError):
                    logger.error(f"Failed to parse AI JSON: {response_text}")
                    raise Exception("AI returned invalid data format")

        except Exception as e:
            logger.error(f"LLM Connection error: {str(e)}")
            raise e

llm_service = LLMService()
