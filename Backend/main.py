from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes.resume import router as resume_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Resume Analyzer API",
    description="API to parse and analyze resumes from PDF/DOCX files",
    version="0.1.0",
)

# Allow frontend applications to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (update for production!)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Register routes
app.include_router(resume_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
