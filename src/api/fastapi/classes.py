from pydantic import BaseModel
from typing import Optional


"""
Input to get recommendation
"""
class Query(BaseModel):
    user_id: str
    top_k: int
    chat_id: Optional[int] = None


"""
A Product Recommendation
"""
class Product(BaseModel):
    product_id: int
    product_name: str
    categories: str
    image_url: str