from app import db
from datetime import datetime
from sqlalchemy import func

class ProductEligibility(db.Model):
    __tablename__ = 'product_eligibility'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False, index=True)
    eligibility_datetime = db.Column(db.DateTime, nullable=False)
    eligibility = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'eligibility_datetime': self.eligibility_datetime.isoformat() if self.eligibility_datetime else None,
            'eligibility': self.eligibility,
            'message': self.message
        }

class ProductSales(db.Model):
    __tablename__ = 'product_sales'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    item_id = db.Column(db.Integer, nullable=False, index=True)
    total_sales = db.Column(db.Float, nullable=False, default=0.0)
    total_units_ordered = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'item_id': self.item_id,
            'total_sales': self.total_sales,
            'total_units_ordered': self.total_units_ordered
        }

class ProductAdMetrics(db.Model):
    __tablename__ = 'product_ad_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    item_id = db.Column(db.Integer, nullable=False, index=True)
    ad_sales = db.Column(db.Float, nullable=False, default=0.0)
    impressions = db.Column(db.Integer, nullable=False, default=0)
    ad_spend = db.Column(db.Float, nullable=False, default=0.0)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    units_sold = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Calculated fields that can be derived from the data
    @property
    def cpc(self):
        """Cost Per Click"""
        return round(self.ad_spend / self.clicks, 2) if self.clicks > 0 else 0.0
    
    @property
    def ctr(self):
        """Click Through Rate as percentage"""
        return round((self.clicks / self.impressions) * 100, 2) if self.impressions > 0 else 0.0
    
    @property
    def roas(self):
        """Return on Ad Spend as percentage"""
        return round((self.ad_sales / self.ad_spend) * 100, 2) if self.ad_spend > 0 else 0.0
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'item_id': self.item_id,
            'ad_sales': self.ad_sales,
            'impressions': self.impressions,
            'ad_spend': self.ad_spend,
            'clicks': self.clicks,
            'units_sold': self.units_sold,
            'cpc': self.cpc,
            'ctr': self.ctr,
            'roas': self.roas
        }
