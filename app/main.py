# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routers import auth_router, authors_router, books_router, borrow_router
from fastapi.middleware.cors import CORSMiddleware

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CreativeScript - Book Library Management API", version="1.0.0")

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth_router.router)
app.include_router(authors_router.router)
app.include_router(books_router.router)
app.include_router(borrow_router.router)

@app.get("/")
def root():
    return {"message": "Library API — go to /docs for interactive API docs"}
