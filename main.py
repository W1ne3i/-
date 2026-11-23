from fastapi import FastAPI, Depends, HTTPException
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

@app.patch(
    "/api/transactions/{transaction_id}",
    response_model=schemas.TransactionResponse
)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Финансовая операция не найдена"
        )

    update_data = transaction_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction

@app.delete("/api/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Финансовая операция не найдена"
        )

    db.delete(transaction)
    db.commit()

    return {
        "message": "Финансовая операция успешно удалена",
        "deleted_id": transaction_id
    }

@app.get("/api/summary", response_model=schemas.SummaryResponse)
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