"""
Project templates with AWS cost breakdowns
"""

from typing import List, Dict
from pydantic import BaseModel


class CostComponent(BaseModel):
    service: str
    description: str
    cost: float


class ProjectTemplate(BaseModel):
    id: int
    name: str
    description: str
    total_cost: float
    components: List[CostComponent]
    estimated_traffic: str
    complexity: str


# Hardcoded project templates (we'll make these dynamic later with AWS Pricing API)
PROJECT_TEMPLATES = [
    ProjectTemplate(
        id=1,
        name="Static Portfolio Website",
        description="HTML/CSS/JS site with global CDN delivery",
        total_cost=1.5,
        components=[
            CostComponent(service="S3", description="Storage (5GB)", cost=0.12),
            CostComponent(service="CloudFront", description="CDN (100GB transfer)", cost=0.85),
            CostComponent(service="Route53", description="DNS hosting", cost=0.50),
        ],
        estimated_traffic="~50K visitors/month",
        complexity="Beginner",
    ),
    ProjectTemplate(
        id=2,
        name="Serverless REST API",
        description="API with database for small apps",
        total_cost=4.5,
        components=[
            CostComponent(service="Lambda", description="100K requests, 128MB, 200ms avg", cost=2.00),
            CostComponent(service="API Gateway", description="100K requests", cost=1.00),
            CostComponent(service="DynamoDB", description="1GB storage, 100K reads/writes", cost=1.25),
            CostComponent(service="CloudWatch", description="Basic logs", cost=0.25),
        ],
        estimated_traffic="~100K API calls/month",
        complexity="Intermediate",
    ),
    ProjectTemplate(
        id=3,
        name="Scheduled Data Scraper",
        description="Run tasks on a schedule, store results",
        total_cost=2.0,
        components=[
            CostComponent(service="Lambda", description="Daily runs, 5 min each", cost=0.50),
            CostComponent(service="EventBridge", description="Scheduled triggers", cost=0.00),
            CostComponent(service="S3", description="Results storage (10GB)", cost=0.25),
            CostComponent(service="DynamoDB", description="Metadata storage", cost=1.25),
        ],
        estimated_traffic="Daily automated tasks",
        complexity="Intermediate",
    ),
    ProjectTemplate(
        id=4,
        name="Small Full-Stack App",
        description="Always-on server with database",
        total_cost=9.5,
        components=[
            CostComponent(service="EC2", description="t4g.nano (ARM, 2 vCPU, 0.5GB RAM)", cost=3.07),
            CostComponent(service="RDS", description="t4g.micro MySQL (1 vCPU, 1GB RAM)", cost=5.84),
            CostComponent(service="EBS", description="20GB SSD storage", cost=0.40),
            CostComponent(service="Data Transfer", description="10GB outbound", cost=0.19),
        ],
        estimated_traffic="~10K users/month",
        complexity="Advanced",
    ),
    ProjectTemplate(
        id=5,
        name="Image Processing Service",
        description="Upload images, auto-resize/optimize",
        total_cost=3.5,
        components=[
            CostComponent(service="Lambda", description="50K invocations, 512MB, 2s avg", cost=2.00),
            CostComponent(service="S3", description="Input/output storage (20GB)", cost=0.50),
            CostComponent(service="S3", description="100K PUT/GET requests", cost=0.50),
            CostComponent(service="CloudWatch", description="Logs", cost=0.50),
        ],
        estimated_traffic="~50K images/month",
        complexity="Intermediate",
    ),
    ProjectTemplate(
        id=6,
        name="Discord/Slack Bot",
        description="Serverless bot responding to commands",
        total_cost=1.0,
        components=[
            CostComponent(service="Lambda", description="20K invocations, 128MB, 100ms", cost=0.40),
            CostComponent(service="API Gateway", description="Webhook endpoint", cost=0.20),
            CostComponent(service="DynamoDB", description="Bot state/config", cost=0.40),
        ],
        estimated_traffic="~20K bot commands/month",
        complexity="Beginner",
    ),
]


def get_projects_by_budget(budget: float) -> Dict:
    """
    Filter projects that fit within the given budget
    
    Args:
        budget: Monthly budget in USD
        
    Returns:
        Dictionary with affordable and expensive projects
    """
    affordable = [p for p in PROJECT_TEMPLATES if p.total_cost <= budget]
    too_expensive = [p for p in PROJECT_TEMPLATES if p.total_cost > budget]
    
    # Calculate some stats
    cheapest = min([p.total_cost for p in affordable]) if affordable else 0
    most_expensive_affordable = max([p.total_cost for p in affordable]) if affordable else 0
    remaining_budget = budget - most_expensive_affordable if affordable else budget
    
    return {
        "budget": budget,
        "affordable_count": len(affordable),
        "affordable_projects": affordable,
        "expensive_projects": too_expensive,
        "stats": {
            "cheapest": cheapest,
            "remaining_budget": remaining_budget,
        }
    }