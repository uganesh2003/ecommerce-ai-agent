import logging
from sqlalchemy import text
from app import db
from gemini import generate_sql_query, format_response
from data_loader import get_database_schema

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
