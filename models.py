from app import db
from datetime import datetime
from sqlalchemy import func

class ProductEligibility(db.Model):
    __tablename__ = 'product_eligibility'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    is_eligible_for_ads = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'brand': self.brand,
            'is_eligible_for_ads': self.is_eligible_for_ads
        }

class ProductSales(db.Model):
    __tablename__ = 'product_sales'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_sales = db.Column(db.Float, nullable=False, default=0.0)
    units_sold = db.Column(db.Integer, nullable=False, default=0)
    revenue = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to eligibility
    product = db.relationship('ProductEligibility', 
                             primaryjoin='ProductSales.product_id == ProductEligibility.product_id',
                             foreign_keys=[product_id], 
                             uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'date': self.date.isoformat() if self.date else None,
            'total_sales': self.total_sales,
            'units_sold': self.units_sold,
            'revenue': self.revenue
        }

class ProductAdMetrics(db.Model):
    __tablename__ = 'product_ad_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    ad_spend = db.Column(db.Float, nullable=False, default=0.0)
    impressions = db.Column(db.Integer, nullable=False, default=0)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    conversions = db.Column(db.Integer, nullable=False, default=0)
    ad_revenue = db.Column(db.Float, nullable=False, default=0.0)
    cpc = db.Column(db.Float, nullable=False, default=0.0)  # Cost Per Click
    ctr = db.Column(db.Float, nullable=False, default=0.0)  # Click Through Rate
    roas = db.Column(db.Float, nullable=False, default=0.0)  # Return on Ad Spend
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to eligibility
    product = db.relationship('ProductEligibility',
                             primaryjoin='ProductAdMetrics.product_id == ProductEligibility.product_id',
                             foreign_keys=[product_id], 
                             uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'date': self.date.isoformat() if self.date else None,
            'ad_spend': self.ad_spend,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'conversions': self.conversions,
            'ad_revenue': self.ad_revenue,
            'cpc': self.cpc,
            'ctr': self.ctr,
            'roas': self.roas
        }
