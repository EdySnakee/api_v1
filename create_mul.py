from sqlmodel import Session
from db import engine
from models import Customer, Transaction


#Para crear multiples transacciones de un cliente
session = Session(engine)
customer = Customer(
    name="Juan Perez",
    description="Cliente de prueba",
    email="mail@mail.com",
    age=30
)

session.add(customer)
session.commit()

#
for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id,
            amount=10 * x,
            description=f"Transacción {x + 1}"
        )
    )
session.commit()
