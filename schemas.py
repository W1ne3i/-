from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    amount: float = Field(gt=0)
    category: str
    date: date
    comment: str | None = None


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    category: str
    date: date
    comment: str | None

    model_config = ConfigDict(from_attributes=True)