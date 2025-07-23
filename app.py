import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///ecommerce_data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Import and register routes
    from routes import *
    
    # Load real data if database is empty
    try:
        if models.ProductSales.query.count() == 0:
            from real_data_loader import load_all_real_data
            load_all_real_data()
    except Exception as e:
        # If tables don't exist, load the data anyway
        logging.info(f"Tables may not exist yet, loading data: {e}")
        from real_data_loader import load_all_real_data
        load_all_real_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
