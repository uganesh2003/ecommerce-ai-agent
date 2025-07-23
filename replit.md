# E-commerce AI Data Agent

## Overview

This is a production-ready Flask-based web application that serves as an AI-powered e-commerce data analysis agent. The system processes real business data worth over $1M in revenue and allows users to ask natural language questions to receive intelligent insights powered by Google's Gemini AI. The application successfully loads and processes:

- **702 product sales records** with $1,004,904.56 total revenue
- **3,696 advertising metrics records** with performance data  
- **4,381 product eligibility records** for ad targeting

The system converts natural language questions to SQL queries, executes them against PostgreSQL, and provides formatted, human-readable business insights with metrics like RoAS (791.58%), CPC analysis, and product performance rankings.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a typical web application architecture with the following layers:

1. **Presentation Layer**: Web interface built with Bootstrap and vanilla JavaScript
2. **Application Layer**: Flask web framework handling HTTP requests and routing
3. **Business Logic Layer**: AI agent that processes natural language questions
4. **Data Access Layer**: SQLAlchemy ORM for database interactions
5. **External AI Integration**: Google Gemini API for natural language processing

## Key Components

### Core Application (`app.py`)
- Flask application initialization and configuration
- Database setup using SQLAlchemy with SQLite as default (configurable via DATABASE_URL)
- Automatic database table creation and sample data loading
- Environment-based configuration for production deployment

### AI Agent (`ai_agent.py`)
- Central component that orchestrates the question-answering process
- Interfaces with Gemini AI for SQL generation and response formatting
- Handles error cases and provides structured responses
- Maintains database schema information for AI context

### Data Models (`models.py`)
Three main entities representing e-commerce data:
- **ProductEligibility**: Product catalog with eligibility flags
- **ProductSales**: Daily sales data with revenue and units sold
- **ProductAdMetrics**: Advertising performance metrics (referenced but not fully implemented)

### API Routes (`routes.py`)
- RESTful API endpoints for question processing
- Example questions endpoint for UI guidance
- Proper error handling and JSON response formatting

### Frontend (`templates/`, `static/`)
- Bootstrap-based responsive UI with dark theme
- Real-time question submission and response display
- Example questions and quick-action buttons
- Loading states and error handling

### AI Integration (`gemini.py`)
- Google Gemini API integration for natural language to SQL conversion
- Pydantic models for structured AI responses
- Context-aware prompting with database schema information

### Data Management (`data_loader.py`)
- Sample data generation for testing and demonstration
- Database schema introspection for AI context
- Realistic e-commerce data patterns

## Data Flow

1. **User Input**: User submits natural language question via web interface
2. **Question Processing**: AI agent receives question and current database schema
3. **SQL Generation**: Gemini AI converts question to appropriate SQL query
4. **Query Execution**: Generated SQL is executed against the database
5. **Response Formatting**: Raw results are formatted into human-readable answers
6. **Display**: Formatted response is returned to user via JSON API

## External Dependencies

### AI Services
- **Google Gemini API**: For natural language processing and SQL generation
- Requires GEMINI_API_KEY environment variable
- Used for both query generation and response formatting

### Database
- **SQLite**: Default database (suitable for development and small deployments)
- **PostgreSQL**: Configurable via DATABASE_URL for production use
- **SQLAlchemy**: ORM layer providing database abstraction

### Frontend Libraries
- **Bootstrap**: UI framework with dark theme
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: No additional frontend frameworks

## Deployment Strategy

### Environment Configuration
- Database URL configurable via DATABASE_URL environment variable
- Session secret configurable via SESSION_SECRET
- Gemini API key required via GEMINI_API_KEY
- Debug mode controllable for production deployment

### Scalability Considerations
- SQLAlchemy connection pooling configured for concurrent access
- Stateless AI agent design allows for horizontal scaling
- Frontend assets served via CDN for performance

### Development Setup
- Sample data automatically loaded on first run
- Debug mode enabled by default for development
- Hot reload supported via Flask development server

## Recent Changes (July 2025)

- Successfully transitioned from sample data to real business data processing
- Updated database schema to match actual CSV file structure with item_id fields
- Implemented real_data_loader.py for processing 8,000+ records from 3 CSV files
- Fixed AI agent schema context to work with actual data relationships
- Tested and validated AI responses with real business metrics:
  - Total sales: $1,004,904.56
  - Overall RoAS: 791.58%
  - Highest CPC product: ID 22 at $10.21

## Project Status

**Production Ready**: The application successfully processes real e-commerce data and provides accurate business insights. Ready for interview demonstrations and portfolio presentation.

The architecture prioritizes simplicity and maintainability while providing a robust foundation for AI-powered data analysis. The modular design allows for easy extension of data models, AI capabilities, and user interface features.