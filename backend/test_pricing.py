"""
Test script to verify AWS pricing API integration
Run with: python test_pricing.py
"""

from app.aws_pricing import AWSPricingClient, calculate_monthly_cost, calculate_lambda_cost


def test_pricing():
    """Test AWS pricing fetching"""
    
    print("🔍 Testing AWS Pricing API Integration\n")
    print("=" * 50)
    
    # Initialize pricing client
    client = AWSPricingClient(region="us-east-1")
    
    # Test EC2 pricing
    print("\n📦 EC2 Pricing:")
    print("-" * 50)
    
    ec2_instances = ['t3.nano', 't3.micro', 't4g.nano', 't4g.micro']
    for instance in ec2_instances:
        price = client.get_ec2_pricing(instance)
        if price:
            monthly = calculate_monthly_cost(price)
            print(f"  {instance:15} ${price:.4f}/hour → ${monthly:.2f}/month")
        else:
            print(f"  {instance:15} ❌ Price not found")
    
    # Test RDS pricing
    print("\n💾 RDS Pricing (MySQL):")
    print("-" * 50)
    
    rds_instances = ['db.t3.micro', 'db.t4g.micro']
    for instance in rds_instances:
        price = client.get_rds_pricing(instance, engine="MySQL")
        if price:
            monthly = calculate_monthly_cost(price)
            print(f"  {instance:15} ${price:.4f}/hour → ${monthly:.2f}/month")
        else:
            print(f"  {instance:15} ❌ Price not found")
    
    # Test Lambda pricing
    print("\n⚡ Lambda Pricing:")
    print("-" * 50)
    
    lambda_pricing = client.get_lambda_pricing()
    print(f"  Per request:      ${lambda_pricing['per_request']:.10f}")
    print(f"  Per GB-second:    ${lambda_pricing['per_gb_second']:.10f}")
    
    # Example calculation
    print("\n  Example: 100K requests, 200ms avg, 128MB memory")
    cost = calculate_lambda_cost(
        requests=100000,
        avg_duration_ms=200,
        memory_mb=128,
        pricing=lambda_pricing
    )
    print(f"  Total cost: ${cost:.2f}/month")
    
    print("\n" + "=" * 50)
    print("✅ Pricing test complete!\n")


if __name__ == "__main__":
    try:
        test_pricing()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: This requires AWS credentials configured.")
        print("If you don't have AWS credentials, that's okay!")
        print("We can use fallback pricing or mock data for now.")