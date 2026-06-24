from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers import auth, notes, pdf, admin

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Notes Generator API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(pdf.router)
app.include_router(admin.router)


@app.get("/")
def home():
    return {
        "message": "AI Notes Generator API Running Successfully"
    }