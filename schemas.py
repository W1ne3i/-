from datetime import date as Date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    amount: float = Field(gt=0)
    category: str
    date: Date
    comment: str | None = None


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    category: str
    date: Date
    comment: str | None

    model_config = ConfigDict(from_attributes=True)

class TransactionUpdate(BaseModel):
    type: Literal["income", "expense"] | None = None
    amount: float | None = Field(default=None, gt=0)
    category: str | None = None
    date: Date | None = None
    comment: str | None = None

class SummaryResponse(BaseModel):
    income: float
    expenses: float
    balance: float