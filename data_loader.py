import logging
from datetime import datetime, date, timedelta
from app import db
from models import ProductEligibility, ProductSales, ProductAdMetrics

def load_sample_data():
    """
    Load sample e-commerce data into the database
    This creates realistic data for testing the AI agent
    """
    try:
        logging.info("Loading sample e-commerce data...")
        
        # Sample products with eligibility data
        products = [
            {"product_id": "PROD001", "product_name": "Wireless Bluetooth Headphones", "category": "Electronics", "brand": "TechBrand"},
            {"product_id": "PROD002", "product_name": "Organic Cotton T-Shirt", "category": "Clothing", "brand": "EcoWear"},
            {"product_id": "PROD003", "product_name": "Stainless Steel Water Bottle", "category": "Sports", "brand": "HydroLife"},
            {"product_id": "PROD004", "product_name": "LED Desk Lamp", "category": "Home", "brand": "BrightLight"},
            {"product_id": "PROD005", "product_name": "Protein Powder Vanilla", "category": "Health", "brand": "FitNutrition"},
        ]
        
        # Create product eligibility records
        for prod_data in products:
            product = ProductEligibility(
                product_id=prod_data["product_id"],
                product_name=prod_data["product_name"],
                category=prod_data["category"],
                brand=prod_data["brand"],
                is_eligible_for_ads=True
            )
            db.session.add(product)
        
        # Generate sales data for the last 30 days
        base_date = date.today() - timedelta(days=30)
        
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            
            for prod_data in products:
                # Generate varying sales data
                base_sales = {
                    "PROD001": {"units": 15, "revenue": 2999.85},
                    "PROD002": {"units": 25, "revenue": 749.75},
                    "PROD003": {"units": 12, "revenue": 359.88},
                    "PROD004": {"units": 8, "revenue": 639.92},
                    "PROD005": {"units": 20, "revenue": 1199.80},
                }
                
                # Add some daily variation (±20%)
                variation = 0.8 + (i % 10) * 0.04  # Creates variation between 0.8 and 1.2
                
                units = int(base_sales[prod_data["product_id"]]["units"] * variation)
                revenue = base_sales[prod_data["product_id"]]["revenue"] * variation
                
                sales = ProductSales(
                    product_id=prod_data["product_id"],
                    date=current_date,
                    total_sales=revenue,
                    units_sold=units,
                    revenue=revenue
                )
                db.session.add(sales)
                
                # Generate ad metrics data
                base_ad_spend = revenue * 0.15  # 15% of revenue as ad spend
                impressions = int(units * 50 * variation)  # 50 impressions per unit sold
                clicks = int(impressions * 0.03)  # 3% CTR
                conversions = int(clicks * 0.1)  # 10% conversion rate
                ad_revenue = revenue * 0.8  # 80% of total revenue attributed to ads
                
                cpc = base_ad_spend / clicks if clicks > 0 else 0
                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                roas = (ad_revenue / base_ad_spend * 100) if base_ad_spend > 0 else 0
                
                ad_metrics = ProductAdMetrics(
                    product_id=prod_data["product_id"],
                    date=current_date,
                    ad_spend=base_ad_spend,
                    impressions=impressions,
                    clicks=clicks,
                    conversions=conversions,
                    ad_revenue=ad_revenue,
                    cpc=round(cpc, 2),
                    ctr=round(ctr, 2),
                    roas=round(roas, 2)
                )
                db.session.add(ad_metrics)
        
        db.session.commit()
        logging.info("Sample data loaded successfully!")
        
    except Exception as e:
        logging.error(f"Error loading sample data: {e}")
        db.session.rollback()
        raise e

def get_database_schema():
    """
    Return database schema information for the AI agent
    """
    schema_info = """
    Tables and their columns:
    
    1. product_eligibility:
       - id (INTEGER, PRIMARY KEY)
       - product_id (VARCHAR(50), UNIQUE)
       - product_name (VARCHAR(200))
       - category (VARCHAR(100))
       - brand (VARCHAR(100))
       - is_eligible_for_ads (BOOLEAN)
       - created_at (DATETIME)
    
    2. product_sales:
       - id (INTEGER, PRIMARY KEY)
       - product_id (VARCHAR(50))
       - date (DATE)
       - total_sales (FLOAT)
       - units_sold (INTEGER)
       - revenue (FLOAT)
       - created_at (DATETIME)
    
    3. product_ad_metrics:
       - id (INTEGER, PRIMARY KEY)
       - product_id (VARCHAR(50))
       - date (DATE)
       - ad_spend (FLOAT)
       - impressions (INTEGER)
       - clicks (INTEGER)
       - conversions (INTEGER)
       - ad_revenue (FLOAT)
       - cpc (FLOAT) -- Cost Per Click
       - ctr (FLOAT) -- Click Through Rate
       - roas (FLOAT) -- Return on Ad Spend
       - created_at (DATETIME)
    
    Note: 
    - product_sales.product_id and product_ad_metrics.product_id reference product_eligibility.product_id
    - Use JOINs to get product names and details
    - RoAS is calculated as (ad_revenue / ad_spend) * 100
    """
    return schema_info
