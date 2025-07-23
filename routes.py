import logging
from flask import render_template, request, jsonify
from app import app
from ai_agent import EcommerceAIAgent
from models import ProductEligibility, ProductSales, ProductAdMetrics

# Initialize AI Agent
ai_agent = EcommerceAIAgent()

@app.route('/')
def index():
    """
    Main page with question interface
    """
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    API endpoint to process natural language questions
    """
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "Question is required"
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty"
            }), 400
        
        # Process the question with AI agent
        result = ai_agent.process_question(question)
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"API error: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/api/examples', methods=['GET'])
def get_example_questions():
    """
    Get example questions and their answers
    """
    try:
        examples = [
            {
                "question": "What is my total sales?",
                "description": "Calculate the sum of all revenue across all products"
            },
            {
                "question": "Calculate the RoAS (Return on Ad Spend)",
                "description": "Calculate the return on advertising spend as a percentage"
            },
            {
                "question": "Which product had the highest CPC (Cost Per Click)?",
                "description": "Find the product with the maximum cost per click"
            },
            {
                "question": "What are my top performing products by revenue?",
                "description": "List products sorted by total revenue"
            },
            {
                "question": "How much did I spend on advertising this month?",
                "description": "Calculate total ad spend for the current period"
            }
        ]
        
        return jsonify({
            "success": True,
            "examples": examples
        })
        
    except Exception as e:
        logging.error(f"Error getting examples: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to load examples"
        }), 500

@app.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    """
    Get summary of available data
    """
    try:
        summary = {
            "total_products": ProductEligibility.query.count(),
            "total_sales_records": ProductSales.query.count(),
            "total_ad_records": ProductAdMetrics.query.count(),
            "date_range": {
                "sales_start": None,
                "sales_end": None
            }
        }
        
        # Get date range safely
        first_sale = ProductSales.query.order_by(ProductSales.date.asc()).first()
        last_sale = ProductSales.query.order_by(ProductSales.date.desc()).first()
        
        if first_sale and last_sale:
            summary["date_range"]["sales_start"] = first_sale.date.isoformat()
            summary["date_range"]["sales_end"] = last_sale.date.isoformat()
        
        return jsonify({
            "success": True,
            "summary": summary
        })
        
    except Exception as e:
        logging.error(f"Error getting data summary: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to load data summary"
        }), 500

@app.route('/api/quick-answers', methods=['GET'])
def get_quick_answers():
    """
    Get quick answers for the demo questions
    """
    try:
        # Process the three main demo questions
        results = {}
        
        # Total sales
        total_sales_result = ai_agent.get_total_sales()
        results['total_sales'] = total_sales_result
        
        # RoAS calculation
        roas_result = ai_agent.calculate_roas()
        results['roas'] = roas_result
        
        # Highest CPC product
        highest_cpc_result = ai_agent.get_highest_cpc_product()
        results['highest_cpc'] = highest_cpc_result
        
        return jsonify({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        logging.error(f"Error getting quick answers: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to generate quick answers"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500
