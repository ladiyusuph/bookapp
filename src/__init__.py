from fastapi import FastAPI
from src.books.routes import book_router

version = "v1"

app = FastAPI(
    version=version,
    description="A CRUD app for book management",
    title="BOOK APP"  
)
app.include_router(book_router, prefix="/api/{version}/books")