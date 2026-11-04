from fastapi import FastAPI, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(title="ВедиБюджет API")


@app.get("/")
def home():
    return {"message": "Backend ВедиБюджет работает!"}


@app.post(
    "/api/transactions",
    response_model=schemas.TransactionResponse
)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    db_transaction = models.Transaction(
        **transaction.model_dump()
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

@app.get(
    "/api/transactions",
    response_model=list[schemas.TransactionResponse]
)
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()

    return transactions

@app.get("/api/summary")
def get_summary(db: Session = Depends(get_db)):
    income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == "income"
    ).scalar() or 0

    expenses = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == "expense"
    ).scalar() or 0

    balance = income - expenses

    return {
        "income": income,
        "expenses": expenses,
        "balance": balance
    }