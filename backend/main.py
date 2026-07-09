from fastapi import FastAPI
from app.routes.delivery_routes import router

app = FastAPI(
    title="Customer Delivery Agent",
    version="1.0.0",
    description="AI Agent that handles package deliveries on behalf of customers."
)
#this creates an interface in http://127.0.0.1:8000/docs to test the API endpoints  

app.include_router(router)


