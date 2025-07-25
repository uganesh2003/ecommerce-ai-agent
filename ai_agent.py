import logging
from sqlalchemy import text
from app import db
from gemini import generate_sql_query, format_response
def get_database_schema():
    """Get comprehensive database schema information for AI context"""
    schema_info = """
    DATABASE SCHEMA:
    
    1. product_sales table:
       - id (Primary Key)
       - date (Date of sales in YYYY-MM-DD format)
       - item_id (Product identifier - integer)
       - total_sales (Total sales amount in dollars - float)
       - total_units_ordered (Number of units ordered - integer)
       - created_at (Timestamp)
    
    2. product_ad_metrics table:
       - id (Primary Key)
       - date (Date of advertising metrics in YYYY-MM-DD format)
       - item_id (Product identifier - integer, matches product_sales.item_id)
       - ad_sales (Revenue from advertising - float)
       - impressions (Number of ad impressions - integer)
       - ad_spend (Amount spent on advertising - float)
       - clicks (Number of ad clicks - integer)
       - units_sold (Number of units sold through ads - integer)
       - created_at (Timestamp)
       
       CALCULATED FIELDS (use these formulas in queries):
       - CPC (Cost Per Click): ad_spend / clicks (when clicks > 0)
       - CTR (Click Through Rate %): (clicks / impressions) * 100 (when impressions > 0)
       - RoAS (Return on Ad Spend %): (ad_sales / ad_spend) * 100 (when ad_spend > 0)
    
    3. product_eligibility table:
       - id (Primary Key)
       - item_id (Product identifier - integer)
       - eligibility_datetime (DateTime when eligibility was checked)
       - eligibility (Boolean - TRUE if eligible for ads, FALSE if not)
       - message (Text explaining eligibility status, empty if eligible)
       - created_at (Timestamp)
    
    IMPORTANT RELATIONSHIPS:
    - All tables are connected via item_id (integer)
    - Use JOINs to get comprehensive product information
    - product_sales contains daily total sales performance
    - product_ad_metrics contains daily advertising performance and metrics
    - product_eligibility contains current advertising eligibility status
    
    SAMPLE QUERIES:
    - Total sales: SELECT SUM(total_sales) FROM product_sales;
    - Total ad spend: SELECT SUM(ad_spend) FROM product_ad_metrics;
    - Overall RoAS: SELECT (SUM(ad_sales)/SUM(ad_spend))*100 FROM product_ad_metrics WHERE ad_spend > 0;
    - Highest CPC product: SELECT item_id, (ad_spend/clicks) as cpc FROM product_ad_metrics WHERE clicks > 0 ORDER BY cpc DESC LIMIT 1;
    - Products by sales: SELECT item_id, SUM(total_sales) as sales FROM product_sales GROUP BY item_id ORDER BY sales DESC;
    """
    return schema_info

class EcommerceAIAgent:
    """
    AI Agent that processes natural language questions about e-commerce data
    """
    
    def __init__(self):
        self.schema_info = get_database_schema()
    
    def process_question(self, question: str) -> dict:
        """
        Process a natural language question and return formatted answer
        """
        try:
            logging.info(f"Processing question: {question}")
            
            # Step 1: Generate SQL query using Gemini
            sql_response = generate_sql_query(question, self.schema_info)
            sql_query = sql_response.query
            explanation = sql_response.explanation
            
            logging.info(f"Generated SQL: {sql_query}")
            
            # Step 2: Execute the SQL query
            result = self.execute_query(sql_query)
            
            # Step 3: Format the response using Gemini
            formatted_answer = format_response(question, result, explanation)
            
            return {
                "success": True,
                "question": question,
                "sql_query": sql_query,
                "explanation": explanation,
                "raw_result": result,
                "formatted_answer": formatted_answer
            }
            
        except Exception as e:
            logging.error(f"Error processing question: {e}")
            return {
                "success": False,
                "question": question,
                "error": str(e),
                "formatted_answer": f"I encountered an error while processing your question: {str(e)}"
            }
    
    def execute_query(self, sql_query: str) -> list:
        """
        Execute SQL query and return results
        """
        try:
            # Execute the query
            result = db.session.execute(text(sql_query))
            
            # Convert result to list of dictionaries
            columns = result.keys()
            rows = result.fetchall()
            
            # Format results
            formatted_results = []
            for row in rows:
                row_dict = {}
                for i, column in enumerate(columns):
                    row_dict[column] = row[i]
                formatted_results.append(row_dict)
            
            logging.info(f"Query executed successfully, returned {len(formatted_results)} rows")
            return formatted_results
            
        except Exception as e:
            logging.error(f"SQL execution error: {e}")
            raise Exception(f"Failed to execute SQL query: {str(e)}")
    
    def get_total_sales(self) -> dict:
        """
        Helper method for total sales calculation
        """
        return self.process_question("What is my total sales?")
    
    def calculate_roas(self) -> dict:
        """
        Helper method for RoAS calculation
        """
        return self.process_question("Calculate the RoAS (Return on Ad Spend)")
    
    def get_highest_cpc_product(self) -> dict:
        """
        Helper method for highest CPC product
        """
        return self.process_question("Which product had the highest CPC (Cost Per Click)?")
