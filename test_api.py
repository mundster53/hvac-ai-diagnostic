"""
Main FastAPI application for HVAC AI Diagnostic.
This is the entry point that starts your web server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import equipment

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered diagnostic and troubleshooting application for HVAC systems",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # Alternative API documentation
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(equipment.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint - basic API info."""
    return {
        "message": "Welcome to HVAC AI Diagnostic API",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": f"{settings.API_V1_STR}/equipment/"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


@app.get("/api/info")
async def api_info():
    """Get information about available API endpoints."""
    return {
        "endpoints": {
            "equipment": {
                "list_all": "GET /api/v1/equipment/",
                "get_one": "GET /api/v1/equipment/{id}",
                "create": "POST /api/v1/equipment/",
                "diagnose": "POST /api/v1/equipment/diagnose",
                "symptoms": "GET /api/v1/equipment/types/{type}/symptoms",
                "stats": "GET /api/v1/equipment/stats/summary"
            }
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }


# This allows you to run the app with: python -m uvicorn src.backend.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.backend.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )