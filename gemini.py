import json
import logging
import os
from google import genai
from google.genai import types
from pydantic import BaseModel

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "default_key"))

class SQLQuery(BaseModel):
    query: str
    explanation: str

def generate_sql_query(question: str, schema_info: str) -> SQLQuery:
    """
    Convert natural language question to SQL query using Gemini
    """
    try:
        system_prompt = f"""
        You are an expert SQL analyst for an e-commerce database. Convert natural language questions to SQL queries.
        
        Database Schema:
        {schema_info}
        
        Rules:
        1. Generate valid SQLite queries only
        2. Use proper table joins when needed
        3. Include appropriate aggregations and filters
        4. Return JSON with 'query' and 'explanation' fields
        5. For RoAS calculations: (ad_revenue / ad_spend) * 100
        6. For total sales: sum revenue from product_sales table
        7. For CPC analysis: use cpc column from product_ad_metrics
        8. Always use proper column names and table aliases
        
        Example questions and expected approach:
        - "What is my total sales?" -> SUM(revenue) FROM product_sales
        - "Calculate the RoAS" -> SELECT (SUM(ad_revenue) / SUM(ad_spend)) * 100 FROM product_ad_metrics
        - "Which product had the highest CPC?" -> SELECT product_id, MAX(cpc) FROM product_ad_metrics
        """

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(role="user", parts=[types.Part(text=f"Question: {question}")])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=SQLQuery,
            ),
        )

        raw_json = response.text
        logging.info(f"Generated SQL JSON: {raw_json}")

        if raw_json:
            data = json.loads(raw_json)
            return SQLQuery(**data)
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to generate SQL query: {e}")
        raise Exception(f"Failed to generate SQL query: {e}")

def format_response(question: str, sql_result: list, explanation: str = "") -> str:
    """
    Format SQL results into human-readable response using Gemini
    """
    try:
        prompt = f"""
        Question: {question}
        SQL Result: {sql_result}
        SQL Explanation: {explanation}
        
        Please format this data into a clear, human-readable answer. 
        Include relevant numbers, percentages, and insights.
        If the result is a single number, present it clearly with context.
        If it's multiple rows, organize the information logically.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text or "Unable to format the response"

    except Exception as e:
        logging.error(f"Failed to format response: {e}")
        return f"Raw data: {sql_result}"
