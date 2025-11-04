"""
AWS Pricing API integration
Fetches real-time pricing data from AWS Price List API
"""

import boto3
import json
from typing import Dict, Optional
from functools import lru_cache


class AWSPricingClient:
    """Client for fetching AWS service pricing"""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize AWS Pricing client
        
        Note: The Pricing API is only available in us-east-1 and ap-south-1
        but returns pricing for all regions
        """
        self.pricing_client = boto3.client('pricing', region_name='us-east-1')
        self.target_region = region
        
    @lru_cache(maxsize=100)
    def get_ec2_pricing(self, instance_type: str) -> Optional[float]:
        """
        Get EC2 instance pricing per hour
        
        Args:
            instance_type: EC2 instance type (e.g., 't3.micro', 't4g.nano')
            
        Returns:
            Price per hour in USD, or None if not found
        """
        try:
            response = self.pricing_client.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'instanceType',
                        'Value': instance_type
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'location',
                        'Value': self._get_region_name(self.target_region)
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'operatingSystem',
                        'Value': 'Linux'
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'tenancy',
                        'Value': 'Shared'
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'preInstalledSw',
                        'Value': 'NA'
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'capacitystatus',
                        'Value': 'Used'
                    }
                ],
                MaxResults=1
            )
            
            if response['PriceList']:
                price_item = json.loads(response['PriceList'][0])
                on_demand = price_item['terms']['OnDemand']
                price_dimensions = list(on_demand.values())[0]['priceDimensions']
                price_per_hour = float(list(price_dimensions.values())[0]['pricePerUnit']['USD'])
                return price_per_hour
            
            return None
            
        except Exception as e:
            print(f"Error fetching EC2 pricing for {instance_type}: {e}")
            return None
    
    @lru_cache(maxsize=100)
    def get_rds_pricing(self, instance_type: str, engine: str = "MySQL") -> Optional[float]:
        """
        Get RDS instance pricing per hour
        
        Args:
            instance_type: RDS instance type (e.g., 'db.t4g.micro')
            engine: Database engine (MySQL, PostgreSQL, etc.)
            
        Returns:
            Price per hour in USD, or None if not found
        """
        try:
            response = self.pricing_client.get_products(
                ServiceCode='AmazonRDS',
                Filters=[
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'instanceType',
                        'Value': instance_type
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'location',
                        'Value': self._get_region_name(self.target_region)
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'databaseEngine',
                        'Value': engine
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'deploymentOption',
                        'Value': 'Single-AZ'
                    }
                ],
                MaxResults=1
            )
            
            if response['PriceList']:
                price_item = json.loads(response['PriceList'][0])
                on_demand = price_item['terms']['OnDemand']
                price_dimensions = list(on_demand.values())[0]['priceDimensions']
                price_per_hour = float(list(price_dimensions.values())[0]['pricePerUnit']['USD'])
                return price_per_hour
            
            return None
            
        except Exception as e:
            print(f"Error fetching RDS pricing for {instance_type}: {e}")
            return None
    
    @lru_cache(maxsize=50)
    def get_lambda_pricing(self) -> Dict[str, float]:
        """
        Get Lambda pricing (requests and compute duration)
        
        Returns:
            Dictionary with 'per_request' and 'per_gb_second' pricing
        """
        try:
            response = self.pricing_client.get_products(
                ServiceCode='AWSLambda',
                Filters=[
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'location',
                        'Value': self._get_region_name(self.target_region)
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'group',
                        'Value': 'AWS-Lambda-Requests'
                    }
                ],
                MaxResults=1
            )
            
            per_request = 0.0000002  # Default fallback
            
            if response['PriceList']:
                price_item = json.loads(response['PriceList'][0])
                on_demand = price_item['terms']['OnDemand']
                price_dimensions = list(on_demand.values())[0]['priceDimensions']
                per_request = float(list(price_dimensions.values())[0]['pricePerUnit']['USD'])
            
            # Lambda compute pricing (per GB-second)
            response = self.pricing_client.get_products(
                ServiceCode='AWSLambda',
                Filters=[
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'location',
                        'Value': self._get_region_name(self.target_region)
                    },
                    {
                        'Type': 'TERM_MATCH',
                        'Field': 'group',
                        'Value': 'AWS-Lambda-Duration'
                    }
                ],
                MaxResults=1
            )
            
            per_gb_second = 0.0000166667  # Default fallback
            
            if response['PriceList']:
                price_item = json.loads(response['PriceList'][0])
                on_demand = price_item['terms']['OnDemand']
                price_dimensions = list(on_demand.values())[0]['priceDimensions']
                per_gb_second = float(list(price_dimensions.values())[0]['pricePerUnit']['USD'])
            
            return {
                'per_request': per_request,
                'per_gb_second': per_gb_second
            }
            
        except Exception as e:
            print(f"Error fetching Lambda pricing: {e}")
            return {
                'per_request': 0.0000002,
                'per_gb_second': 0.0000166667
            }
    
    def _get_region_name(self, region_code: str) -> str:
        """
        Convert region code to AWS Pricing API region name
        
        Args:
            region_code: AWS region code (e.g., 'us-east-1')
            
        Returns:
            Region name for Pricing API (e.g., 'US East (N. Virginia)')
        """
        region_map = {
            'us-east-1': 'US East (N. Virginia)',
            'us-east-2': 'US East (Ohio)',
            'us-west-1': 'US West (N. California)',
            'us-west-2': 'US West (Oregon)',
            'eu-west-1': 'EU (Ireland)',
            'eu-central-1': 'EU (Frankfurt)',
            'ap-southeast-1': 'Asia Pacific (Singapore)',
            'ap-southeast-2': 'Asia Pacific (Sydney)',
            'ap-northeast-1': 'Asia Pacific (Tokyo)',
        }
        return region_map.get(region_code, 'US East (N. Virginia)')


def calculate_monthly_cost(hourly_price: float, hours_per_month: int = 730) -> float:
    """
    Calculate monthly cost from hourly price
    
    Args:
        hourly_price: Price per hour
        hours_per_month: Hours in a month (default: 730, which is ~30.4 days)
        
    Returns:
        Monthly cost
    """
    return hourly_price * hours_per_month


def calculate_lambda_cost(
    requests: int,
    avg_duration_ms: int,
    memory_mb: int,
    pricing: Dict[str, float]
) -> float:
    """
    Calculate Lambda cost based on usage
    
    Args:
        requests: Number of requests
        avg_duration_ms: Average duration in milliseconds
        memory_mb: Memory allocation in MB
        pricing: Lambda pricing dictionary from get_lambda_pricing()
        
    Returns:
        Total cost
    """
    # Request cost
    request_cost = requests * pricing['per_request']
    
    # Compute cost
    gb_seconds = (memory_mb / 1024) * (avg_duration_ms / 1000) * requests
    compute_cost = gb_seconds * pricing['per_gb_second']
    
    # Free tier: 1M requests + 400,000 GB-seconds per month
    # For simplicity, we're not accounting for free tier here
    
    return request_cost + compute_cost