# models.py

from typing import List, Tuple
from pydantic import BaseModel

class TestRequest(BaseModel):
    hotel_name: str
    date_ranges: List[Tuple[str, str]]
