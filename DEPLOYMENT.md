# Deployment Guide

## Interview Demonstration Setup

### Quick Demo Setup
1. **Environment Variables Required:**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   GEMINI_API_KEY=your_gemini_api_key
   SESSION_SECRET=random_secret_key
   ```

2. **Run Application:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

3. **Test API Endpoints:**
   ```bash
   # Total sales
   curl -X POST http://localhost:5000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is my total sales?"}'
   
   # RoAS calculation
   curl -X POST http://localhost:5000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "Calculate the RoAS"}'
   ```

## Production Deployment Options

### Option 1: Replit Deployments
- One-click deployment
- Automatic SSL/TLS
- Built-in monitoring
- Custom domain support

### Option 2: Cloud Platforms
- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repository
- **Render**: Auto-deploy from Git
- **DigitalOcean App Platform**: Container deployment

### Option 3: Traditional VPS
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip postgresql

# Setup application
git clone <repo-url>
cd ecommerce-ai-agent
pip3 install -r requirements.txt

# Configure database
sudo -u postgres createdb ecommerce_ai

# Start with systemd
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

## Environment Configuration

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY`: Google AI API key
- `SESSION_SECRET`: Flask session security key

### Optional Configuration
- `DEBUG`: Set to `False` for production
- `PORT`: Application port (default: 5000)
- `WORKERS`: Gunicorn worker processes

## Database Setup

### PostgreSQL Schema
Tables are created automatically on first run:
- `product_sales`
- `product_ad_metrics` 
- `product_eligibility`

### Data Loading
CSV files in `attached_assets/` are loaded automatically:
- Product-Level Total Sales and Metrics
- Product-Level Ad Sales and Metrics  
- Product-Level Eligibility Table

## Monitoring & Logging

### Application Logs
- SQL query generation
- AI processing steps
- Error tracking
- Performance metrics

### Health Checks
- Database connectivity
- AI service availability
- Data integrity validation

## Security Considerations

### Production Checklist
- [ ] Environment variables secured
- [ ] Database connections encrypted
- [ ] API rate limiting implemented
- [ ] Input validation enabled
- [ ] Error messages sanitized
- [ ] HTTPS enforced
- [ ] Session security configured

### API Security
- SQL injection prevention via parameterized queries
- Input sanitization for natural language processing
- Error handling without data exposure