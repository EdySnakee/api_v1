from datetime import datetime
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select

#modelos
from db import create_all_tables
from .routers import customer, transactions, invoices, plans


app = FastAPI(lifespan=create_all_tables)

app.include_router(customer.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = datetime.now()
    response = await call_next(request)
    duration = datetime.now() - start
    print(f"Request: {request.url} compleded in: {duration} seconds")
    return response


security = HTTPBasic()
@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == "admin" and credentials.password == "1234":
        return {"message": "Esto podria ser el hom de una aplicacion"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")



#para regresar el tiempo
@app.get("/time")
async def get_time():
    return {"tiem": datetime.now()}


