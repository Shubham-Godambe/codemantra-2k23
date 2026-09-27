"""
CODEMANTRA 2K23 - AI-Based Tree Enumeration and Forest Land Analysis
Main FastAPI application.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routes
from app.routes import upload, detection, analysis

# Create FastAPI app
app = FastAPI(
    title="CODEMANTRA 2K23",
    description="AI-Assisted Tree Enumeration and Forest Land Analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(detection.router)
app.include_router(analysis.router)

# Serve static files
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    """Serve dashboard."""
    return FileResponse("app/templates/index.html", media_type="text/html")


@app.get("/results")
async def results_page():
    """Serve results page."""
    return FileResponse("app/templates/results.html", media_type="text/html")


@app.get("/map")
async def map_page():
    """Serve map page."""
    return FileResponse("app/templates/map.html", media_type="text/html")


@app.get("/about")
async def about_page():
    """Serve about page."""
    return FileResponse("app/templates/about.html", media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
