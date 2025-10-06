from pydantic import BaseModel, Field
from typing import List, Optional

class Node(BaseModel):
    id: str
    text: str
    type: Optional[str] = Field("or", description="'or' or 'and'")
    children: List[str] = []
    probability: Optional[float] = None
    cost: Optional[float] = None
    defense: Optional[str] = None

class AttackTree(BaseModel):
    goal: str
    nodes: List[Node]
