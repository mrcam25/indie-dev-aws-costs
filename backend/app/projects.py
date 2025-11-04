"""
Project templates with AWS cost breakdowns
Now with live AWS pricing!
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from app.aws_pricing import (
    AWSPricingClient, 
    calculate_monthly_cost, 
    calculate_lambda_cost
)


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
    pricing_source: str = "live"  # "live" or "fallback"


# Initialize pricing client (will be reused across requests)
pricing_client: Optional[AWSPricingClient] = None

def get_pricing_client() -> AWSPricingClient:
    """Get or create pricing client singleton"""
    global pricing_client
    if pricing_client is None:
        pricing_client = AWSPricingClient(region="us-east-1")
    return pricing_client


def get_live_project_templates() -> List[ProjectTemplate]:
    """
    Generate project templates with live AWS pricing
    Falls back to hardcoded pricing if AWS API fails
    """
    client = get_pricing_client()
    pricing_source = "live"
    
    try:
        # Fetch live pricing
        lambda_pricing = client.get_lambda_pricing()
        
        # EC2 + RDS for full-stack app
        ec2_t4g_nano_hourly = client.get_ec2_pricing("t4g.nano") or 0.0042
        rds_t4g_micro_hourly = client.get_rds_pricing("db.t4g.micro", "MySQL") or 0.0160
        
        # Calculate monthly costs
        ec2_monthly = calculate_monthly_cost(ec2_t4g_nano_hourly)
        rds_monthly = calculate_monthly_cost(rds_t4g_micro_hourly)
        
        # Lambda costs for various scenarios
        lambda_100k_128mb_200ms = calculate_lambda_cost(
            requests=100000,
            avg_duration_ms=200,
            memory_mb=128,
            pricing=lambda_pricing
        )
        
        lambda_50k_512mb_2000ms = calculate_lambda_cost(
            requests=50000,
            avg_duration_ms=2000,
            memory_mb=512,
            pricing=lambda_pricing
        )
        
        lambda_20k_128mb_100ms = calculate_lambda_cost(
            requests=20000,
            avg_duration_ms=100,
            memory_mb=128,
            pricing=lambda_pricing
        )
        
        lambda_daily_scraper = calculate_lambda_cost(
            requests=30,  # Once per day
            avg_duration_ms=300000,  # 5 minutes
            memory_mb=256,
            pricing=lambda_pricing
        )
        
    except Exception as e:
        print(f"⚠️  Failed to fetch live pricing: {e}")
        print("📊 Using fallback pricing")
        pricing_source = "fallback"
        
        # Fallback to hardcoded pricing
        ec2_monthly = 3.07
        rds_monthly = 11.68
        lambda_100k_128mb_200ms = 2.00
        lambda_50k_512mb_2000ms = 2.00
        lambda_20k_128mb_100ms = 0.40
        lambda_daily_scraper = 0.50
    
    # Build project templates with calculated pricing
    templates = [
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
            pricing_source=pricing_source,
        ),
        ProjectTemplate(
            id=2,
            name="Serverless REST API",
            description="API with database for small apps",
            total_cost=round(lambda_100k_128mb_200ms + 1.00 + 1.25 + 0.25, 2),
            components=[
                CostComponent(
                    service="Lambda", 
                    description="100K requests, 128MB, 200ms avg", 
                    cost=round(lambda_100k_128mb_200ms, 2)
                ),
                CostComponent(service="API Gateway", description="100K requests", cost=1.00),
                CostComponent(service="DynamoDB", description="1GB storage, 100K reads/writes", cost=1.25),
                CostComponent(service="CloudWatch", description="Basic logs", cost=0.25),
            ],
            estimated_traffic="~100K API calls/month",
            complexity="Intermediate",
            pricing_source=pricing_source,
        ),
        ProjectTemplate(
            id=3,
            name="Scheduled Data Scraper",
            description="Run tasks on a schedule, store results",
            total_cost=round(lambda_daily_scraper + 0.25 + 1.25, 2),
            components=[
                CostComponent(
                    service="Lambda", 
                    description="Daily runs, 5 min each", 
                    cost=round(lambda_daily_scraper, 2)
                ),
                CostComponent(service="EventBridge", description="Scheduled triggers", cost=0.00),
                CostComponent(service="S3", description="Results storage (10GB)", cost=0.25),
                CostComponent(service="DynamoDB", description="Metadata storage", cost=1.25),
            ],
            estimated_traffic="Daily automated tasks",
            complexity="Intermediate",
            pricing_source=pricing_source,
        ),
        ProjectTemplate(
            id=4,
            name="Small Full-Stack App",
            description="Always-on server with database",
            total_cost=round(ec2_monthly + rds_monthly + 0.40 + 0.19, 2),
            components=[
                CostComponent(
                    service="EC2", 
                    description="t4g.nano (ARM, 2 vCPU, 0.5GB RAM)", 
                    cost=round(ec2_monthly, 2)
                ),
                CostComponent(
                    service="RDS", 
                    description="t4g.micro MySQL (1 vCPU, 1GB RAM)", 
                    cost=round(rds_monthly, 2)
                ),
                CostComponent(service="EBS", description="20GB SSD storage", cost=0.40),
                CostComponent(service="Data Transfer", description="10GB outbound", cost=0.19),
            ],
            estimated_traffic="~10K users/month",
            complexity="Advanced",
            pricing_source=pricing_source,
        ),
        ProjectTemplate(
            id=5,
            name="Image Processing Service",
            description="Upload images, auto-resize/optimize",
            total_cost=round(lambda_50k_512mb_2000ms + 0.50 + 0.50 + 0.50, 2),
            components=[
                CostComponent(
                    service="Lambda", 
                    description="50K invocations, 512MB, 2s avg", 
                    cost=round(lambda_50k_512mb_2000ms, 2)
                ),
                CostComponent(service="S3", description="Input/output storage (20GB)", cost=0.50),
                CostComponent(service="S3", description="100K PUT/GET requests", cost=0.50),
                CostComponent(service="CloudWatch", description="Logs", cost=0.50),
            ],
            estimated_traffic="~50K images/month",
            complexity="Intermediate",
            pricing_source=pricing_source,
        ),
        ProjectTemplate(
            id=6,
            name="Discord/Slack Bot",
            description="Serverless bot responding to commands",
            total_cost=round(lambda_20k_128mb_100ms + 0.20 + 0.40, 2),
            components=[
                CostComponent(
                    service="Lambda", 
                    description="20K invocations, 128MB, 100ms", 
                    cost=round(lambda_20k_128mb_100ms, 2)
                ),
                CostComponent(service="API Gateway", description="Webhook endpoint", cost=0.20),
                CostComponent(service="DynamoDB", description="Bot state/config", cost=0.40),
            ],
            estimated_traffic="~20K bot commands/month",
            complexity="Beginner",
            pricing_source=pricing_source,
        ),
    ]
    
    return templates


def get_projects_by_budget(budget: float) -> Dict:
    """
    Filter projects that fit within the given budget
    Uses live AWS pricing when available
    
    Args:
        budget: Monthly budget in USD
        
    Returns:
        Dictionary with affordable and expensive projects
    """
    all_projects = get_live_project_templates()
    
    affordable = [p for p in all_projects if p.total_cost <= budget]
    too_expensive = [p for p in all_projects if p.total_cost > budget]
    
    # Calculate some stats
    cheapest = min([p.total_cost for p in affordable]) if affordable else 0
    most_expensive_affordable = max([p.total_cost for p in affordable]) if affordable else 0
    remaining_budget = budget - most_expensive_affordable if affordable else budget
    
    # Check pricing source
    pricing_source = all_projects[0].pricing_source if all_projects else "unknown"
    
    return {
        "budget": budget,
        "affordable_count": len(affordable),
        "affordable_projects": affordable,
        "expensive_projects": too_expensive,
        "stats": {
            "cheapest": cheapest,
            "remaining_budget": remaining_budget,
        },
        "pricing_source": pricing_source,
        "pricing_note": "Live AWS pricing" if pricing_source == "live" else "Using fallback pricing (AWS API unavailable)"
    }