from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float
    tags: List[str]

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    products: List[Product]
    summary: str

class LLMRecommendation(BaseModel):
    productIds: List[int]
    summary: str
