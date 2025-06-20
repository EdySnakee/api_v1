from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
from db import SessionDep
from models import Customer, Transaction, TransactionCreate

router = APIRouter()

@router.post("/transactions", status_code=status.HTTP_201_CREATED, tags=["Transactions"])
async def create_transaction(transactions_data: TransactionCreate, session: SessionDep):
    transactions_data_dict = transactions_data.model_dump()
    customer = session.get(Customer, transactions_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    transaction_db = Transaction.model_validate(transactions_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("/transactions", tags=["Transactions"])
async def list_transactions(session: SessionDep, skip: int = Query(0, description="Registros a omitir"), limit: int = Query(10, description="Cantidad de registros")):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions


