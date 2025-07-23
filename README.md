<<<<<<< HEAD
# E-commerce AI Data Agent

An AI-powered e-commerce data analysis agent that converts natural language questions into SQL queries and provides intelligent business insights using Google's Gemini AI.

## 🚀 Live Demo

This application processes real e-commerce data including:
- **702 product sales records** with $1,004,904.56 total revenue
- **3,696 advertising metrics records** with performance data
- **4,381 product eligibility records** for ad targeting

## 🎯 Key Features

- **Natural Language Processing**: Ask questions in plain English
- **SQL Generation**: Automatically converts questions to optimized SQL queries
- **Real-time Analytics**: Instant insights from your actual business data
- **Performance Metrics**: RoAS, CPC, CTR calculations and analysis
- **Responsive Web Interface**: Clean, professional dashboard

## 🏗️ Architecture

```
Flask Web Application
├── Frontend (Bootstrap + Vanilla JS)
├── API Layer (RESTful endpoints)
├── AI Agent (Google Gemini integration)
├── Data Layer (PostgreSQL + SQLAlchemy)
└── Business Logic (Analytics & Calculations)
```

## 📊 Example Queries & Results

| Question | Result |
|----------|--------|
| "What is my total sales?" | $1,004,904.56 total revenue |
| "Calculate the RoAS" | 791.58% return on ad spend |
| "Which product had the highest CPC?" | Product ID 22 at $10.21 per click |

## 🛠️ Technology Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: PostgreSQL
- **AI/ML**: Google Gemini AI (2.5-Pro, 2.5-Flash)
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Data Processing**: Pandas, CSV parsing
- **Deployment**: Gunicorn WSGI server

## 📁 Project Structure

```
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models (SQLAlchemy)
├── routes.py           # API endpoints and routing
├── ai_agent.py         # Core AI processing logic
├── gemini.py           # Google Gemini AI integration
├── real_data_loader.py # CSV data processing
├── templates/
│   └── index.html      # Web interface
├── static/             # CSS, JS, assets
└── attached_assets/    # Source CSV data files
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Google Gemini API key

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
GEMINI_API_KEY=your_gemini_api_key_here
SESSION_SECRET=your_session_secret
```

### Installation Steps
```bash
# Clone repository
git clone <your-repo-url>
cd ecommerce-ai-agent

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your_database_url"
export GEMINI_API_KEY="your_api_key"

# Run application
gunicorn --bind 0.0.0.0:5000 main:app
```

## 🧠 AI Agent Workflow

1. **Question Processing**: Receives natural language input
2. **Schema Analysis**: Reviews database structure and relationships
3. **SQL Generation**: Uses Gemini to create optimized queries
4. **Query Execution**: Safely executes SQL against PostgreSQL
5. **Response Formatting**: Converts results to human-readable insights

## 📈 Business Intelligence Features

### Sales Analytics
- Total revenue calculation
- Product performance ranking
- Time-based sales trends
- Unit volume analysis

### Advertising Metrics
- Return on Ad Spend (RoAS)
- Cost Per Click (CPC) analysis
- Click-Through Rate (CTR) optimization
- Campaign performance insights

### Product Intelligence
- Eligibility status tracking
- Performance correlation analysis
- Revenue attribution
- Cross-product analytics

## 🔍 Technical Highlights

### Data Processing
- Handles large CSV datasets (4,000+ records)
- Efficient batch loading with progress tracking
- Data validation and type conversion
- Automatic schema detection

### AI Integration
- Context-aware SQL generation
- Error handling and query optimization
- Natural language response formatting
- Multi-model AI architecture (Pro + Flash)

### Security & Performance
- SQL injection prevention via parameterized queries
- Connection pooling for database efficiency
- Environment-based configuration
- Error logging and monitoring

## 🎤 Interview Talking Points

### Problem Solved
"This project addresses the challenge of making business data accessible to non-technical stakeholders. Instead of requiring SQL knowledge, users can ask questions in natural language and get instant, accurate insights."

### Technical Decisions
- **Why Gemini AI**: Superior natural language understanding and SQL generation capabilities
- **Why PostgreSQL**: Robust relational database with excellent performance for analytics
- **Why Flask**: Lightweight, flexible framework perfect for API-first architecture

### Scalability Considerations
- Stateless AI agent design enables horizontal scaling
- Database connection pooling handles concurrent users
- Modular architecture allows easy feature extension

### Real-World Impact
- Processes actual business data worth over $1M in revenue
- Provides actionable insights with 791% RoAS analysis
- Enables data-driven decision making for e-commerce teams

## 📊 Data Schema

### ProductSales
- Daily sales records with revenue and unit data
- Date-based partitioning for time series analysis

### ProductAdMetrics  
- Advertising performance with spend, clicks, impressions
- Calculated fields for CPC, CTR, RoAS metrics

### ProductEligibility
- Real-time eligibility status for advertising
- Message fields for detailed status explanations

## 🚀 Future Enhancements

- [ ] Dashboard visualizations with Chart.js
- [ ] Email report automation
- [ ] Multi-tenant support
- [ ] Advanced predictive analytics
- [ ] Integration with advertising platforms

## 📝 License

This project is available for demonstration and portfolio purposes.

---

**Built with ❤️ using Python, Flask, and Google Gemini AI**
=======
# ecommerce-ai-agent
AI-powered e-commerce data analysis agent with natural language to SQL conversion
>>>>>>> 32b7160e2394f7b86be9b716ddac828a7a7b9a45
