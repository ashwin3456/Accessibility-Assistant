from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.visual import router as visual_router


# --------------------------------------------------
# CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="FASAL FLOW AI Backend",
    description="AI Accessibility Assistant Backend",
    version="1.0.0"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# --------------------------------------------------
# VISUAL ASSISTANCE ROUTES
# --------------------------------------------------

app.include_router(
    visual_router
)


# --------------------------------------------------
# HOME / ROOT API
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "FASAL FLOW AI Backend is running",
        "service": "Accessibility Assistant"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "message": "Backend is working correctly"
    }


# --------------------------------------------------
# SERVER INFORMATION
# --------------------------------------------------

@app.get("/api/info")
def info():

    return {
        "project": "FASAL FLOW",
        "module": "Accessibility Assistant",
        "features": [
            "Object Detection",
            "Obstacle Detection",
            "Sign Detection",
            "OCR",
            "Visual Assistance"
        ]
    }