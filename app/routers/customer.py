from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
#modelos
from db import SessionDep
from models import Customer, CustomerCreate, CustomerUpdate, Plan, PlanCustomer, StatusEnum


router = APIRouter()

# Crear usuario
@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def create_customer(customer_data: CustomerCreate, session:SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# TRAER usuario por Id
@router.get("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

# EDITAR usuario por Id
@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def edit_customer(customer_id: int, customer_data:CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

# BORRAR usuario por Id
@router.delete("/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {
        "detail:": "Customer deleted successfully",
    }

# LIST de usuarios
@router.get("/customers", response_model=list[Customer], tags=["Customers"])
async def list_customers(session: SessionDep):
   return session.exec(select(Customer)).all()

# Usuario -> Plan
@router.post("/customer/{customer_id}/plans/{plan_id}", tags=["Customers"])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer or Plan not found")
    
    customer_plan_db = PlanCustomer(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


# Listar Planes de un usuario
@router.get("/customers/{customer_id}/plans", tags=["Customers"])
async def list_customer_to_plan(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    
    customer_db = session.get(Customer, customer_id)
    
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    query = select(PlanCustomer).where(PlanCustomer.customer_id == customer_id).where(PlanCustomer.status == plan_status)
    plans = session.exec(query).all()
    
    return plans