"""
FastAPI backend for AWS Budget Planner
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.projects import get_projects_by_budget, get_live_project_templates

app = FastAPI(
    title="AWS Budget Planner API",
    description="API for calculating AWS project costs within budget",
    version="0.1.0",
)

# Enable CORS so your React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AWS Budget Planner API",
        "version": "0.1.0",
    }


@app.get("/api/projects")
def get_projects(
    budget: float = Query(
        default=10.0,
        ge=1.0,
        le=10000.0,
        description="Monthly budget in USD"
    )
):
    """
    Get project templates filtered by budget
    
    Args:
        budget: Monthly budget in USD (default: $10)
        
    Returns:
        Projects within budget and statistics
    """
    return get_projects_by_budget(budget)


@app.get("/api/projects/all")
def get_all_projects():
    """
    Get all available project templates with live pricing
    
    Returns:
        List of all project templates
    """
    from app.projects import get_live_project_templates
    
    projects = get_live_project_templates()
    pricing_source = projects[0].pricing_source if projects else "unknown"
    
    return {
        "count": len(projects),
        "projects": projects,
        "pricing_source": pricing_source,
    }


@app.get("/api/health")
def health_check():
    """Detailed health check"""
    projects = get_live_project_templates()
    
    return {
        "status": "healthy",
        "projects_loaded": len(projects),
        "pricing_source": projects[0].pricing_source if projects else "unknown",
        "endpoints": [
            "GET /",
            "GET /api/projects?budget=10",
            "GET /api/projects/all",
            "GET /api/health",
        ]
    }