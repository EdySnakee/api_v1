from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import Relationship, SQLModel, Field, Session, select
from db import engine


# Status Enum for PlanCustomer
class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# PLAN CUSTOMER
class PlanCustomer(SQLModel, table=True):
    id:int = Field(primary_key=True)
    plan_id:int = Field(foreign_key="plan.id")
    customer_id:int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)   


#PLAN
class Plan(SQLModel, table=True):
    id:int | None = Field(primary_key=True)
    name:str = Field(max_length=100, default=None)
    price:int = Field(default=None)
    description:str | None = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=PlanCustomer
    )


# CUSTOMER
class CustomerBase(SQLModel):
    name:str = Field(default=None, max_length=100)
    description:str | None = Field(default=None)
    email:EmailStr = Field(default=None)
    age:int = Field(default=None)
    
    @field_validator("email")
    @classmethod
    def validate_amail(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("Email already exists")
        return value
       
class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    transactions:list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=PlanCustomer
    )


# TRANSACTION
class TransactionBase(SQLModel):
    amount:int
    description:str | None

class Transaction(TransactionBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    customer_id:int = Field(foreign_key="customer.id")
    customer : Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    customer_id:int = Field(foreign_key="customer.id")
    

# INVOICE
class Invoice(BaseModel):
    id:int
    customer: Customer
    transactions: list[Transaction]
    total: int
    
    @property
    def total_amount(self) -> int:
        return sum(transaction.amount for transaction in self.transactions)