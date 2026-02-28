from fastapi import APIRouter, HTTPException
import traceback
from typing import List, Optional
from app.models import Product, AskRequest, AskResponse
from app.services.retrieval_service import retrieval_service
from app.services.llm_service import llm_service

router = APIRouter(prefix="/api")

@router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None):
    try:
        return retrieval_service.get_all_products(category)
    except Exception:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/ask", response_model=AskResponse)
async def ask_product(request: AskRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Step 1: Retrieve top relevant products via keyword scoring
        retrieved_products = retrieval_service.retrieve_top_products(request.query)
        
        # Step 2 & 3: Get recommendation and summary from LLM
        recommendation = await llm_service.get_recommendations(request.query, retrieved_products)
        
        # Step 4: Map productIds back to full product objects
        all_products = retrieval_service.get_all_products()
        recommended_products = [p for p in all_products if p.id in recommendation.productIds]
        
        # Step 5: Return structured response
        return AskResponse(
            products=recommended_products,
            summary=recommendation.summary
        )
    except Exception as e:
        print(f"--- [CRITICAL ERROR] {str(e)}")
        print(traceback.format_exc())
        # Step 5: Error handling - 502 if LLM fails (mapped in llm_service or here)
        raise HTTPException(status_code=502, detail=f"AI Error: {str(e)}")
