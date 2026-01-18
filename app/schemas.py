from datetime import date
from pydantic import BaseModel

class AssetBase(BaseModel):
    name: str
    category: str
    value: float
    purchase_date: date
    status: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass

class AssetOut(AssetBase):
    id: int

    class Config:
        from_attributes = True

class AgentRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    answer: str
    sources: list[str] = []
