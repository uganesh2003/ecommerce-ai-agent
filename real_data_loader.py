import csv
import os
from datetime import datetime

def parse_datetime(datetime_str):
    """Parse datetime string from CSV format"""
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Try alternative format if the first one fails
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d')
        except ValueError:
            return None

def load_product_sales_data():
    """Load product sales data from CSV"""
    from app import db
    from models import ProductSales
    
    file_path = "attached_assets/Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped)_1753244242358.csv"
    
    if not os.path.exists(file_path):
        print(f"Sales data file not found: {file_path}")
        return
    
    print("Loading product sales data...")
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Parse date
                date_obj = datetime.strptime(row['date'], '%Y-%m-%d').date()
                
                # Convert values
                item_id = int(row['item_id'])
                total_sales = float(row['total_sales']) if row['total_sales'] else 0.0
                total_units_ordered = int(row['total_units_ordered']) if row['total_units_ordered'] else 0
                
                # Create record
                sales_record = ProductSales(
                    date=date_obj,
                    item_id=item_id,
                    total_sales=total_sales,
                    total_units_ordered=total_units_ordered
                )
                
                db.session.add(sales_record)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
                    print(f"Loaded {count} sales records...")
                    
            except (ValueError, KeyError) as e:
                print(f"Error processing sales row: {row}, Error: {e}")
                continue
    
    db.session.commit()
    print(f"Successfully loaded {count} product sales records")

def load_product_ad_metrics_data():
    """Load product ad metrics data from CSV"""
    from app import db
    from models import ProductAdMetrics
    
    file_path = "attached_assets/Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped)_1753244242359.csv"
    
    if not os.path.exists(file_path):
        print(f"Ad metrics data file not found: {file_path}")
        return
    
    print("Loading product ad metrics data...")
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Parse date
                date_obj = datetime.strptime(row['date'], '%Y-%m-%d').date()
                
                # Convert values
                item_id = int(row['item_id'])
                ad_sales = float(row['ad_sales']) if row['ad_sales'] else 0.0
                impressions = int(row['impressions']) if row['impressions'] else 0
                ad_spend = float(row['ad_spend']) if row['ad_spend'] else 0.0
                clicks = int(row['clicks']) if row['clicks'] else 0
                units_sold = int(row['units_sold']) if row['units_sold'] else 0
                
                # Create record
                ad_record = ProductAdMetrics(
                    date=date_obj,
                    item_id=item_id,
                    ad_sales=ad_sales,
                    impressions=impressions,
                    ad_spend=ad_spend,
                    clicks=clicks,
                    units_sold=units_sold
                )
                
                db.session.add(ad_record)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
                    print(f"Loaded {count} ad metrics records...")
                    
            except (ValueError, KeyError) as e:
                print(f"Error processing ad metrics row: {row}, Error: {e}")
                continue
    
    db.session.commit()
    print(f"Successfully loaded {count} product ad metrics records")

def load_product_eligibility_data():
    """Load product eligibility data from CSV"""
    from app import db
    from models import ProductEligibility
    
    file_path = "attached_assets/Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped)_1753244242361.csv"
    
    if not os.path.exists(file_path):
        print(f"Eligibility data file not found: {file_path}")
        return
    
    print("Loading product eligibility data...")
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Parse datetime
                datetime_obj = parse_datetime(row['eligibility_datetime_utc'])
                if not datetime_obj:
                    print(f"Could not parse datetime: {row['eligibility_datetime_utc']}")
                    continue
                
                # Convert values
                item_id = int(row['item_id'])
                eligibility = row['eligibility'].upper() == 'TRUE'
                message = row['message'].strip() if row['message'] else None
                
                # Create record
                eligibility_record = ProductEligibility(
                    item_id=item_id,
                    eligibility_datetime=datetime_obj,
                    eligibility=eligibility,
                    message=message
                )
                
                db.session.add(eligibility_record)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
                    print(f"Loaded {count} eligibility records...")
                    
            except (ValueError, KeyError) as e:
                print(f"Error processing eligibility row: {row}, Error: {e}")
                continue
    
    db.session.commit()
    print(f"Successfully loaded {count} product eligibility records")

def load_all_real_data():
    """Load all real data from CSV files"""
    # Import within function to avoid circular imports
    from app import db
    from models import ProductSales, ProductAdMetrics, ProductEligibility
    
    print("Starting to load real e-commerce data...")
    
    # Clear existing data
    print("Clearing existing data...")
    ProductSales.query.delete()
    ProductAdMetrics.query.delete() 
    ProductEligibility.query.delete()
    db.session.commit()
    
    # Load new data
    load_product_sales_data()
    load_product_ad_metrics_data()
    load_product_eligibility_data()
    
    print("All real data loaded successfully!")
    
    # Print summary statistics
    sales_count = ProductSales.query.count()
    ad_count = ProductAdMetrics.query.count()
    eligibility_count = ProductEligibility.query.count()
    
    print(f"\nData Summary:")
    print(f"- Product Sales Records: {sales_count}")
    print(f"- Product Ad Metrics Records: {ad_count}")
    print(f"- Product Eligibility Records: {eligibility_count}")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        load_all_real_data()