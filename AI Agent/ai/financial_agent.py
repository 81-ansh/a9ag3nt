# ai/financial_agent.py
import google.generativeai as genai
import pandas as pd
from typing import Dict, List, Any, Optional
import json
import logging
from database.db_manager import DatabaseManager

class FinancialAIAgent:
    """AI Agent for financial analysis and database operations"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
        
        # Financial consolidation context
        self.system_prompt = """
        You are an expert financial consolidation AI assistant. You have access to Oracle database 
        with financial data. You can:
        1. Analyze financial statements and variances
        2. Generate SQL queries for financial data
        3. Perform consolidation calculations
        4. Detect anomalies and discrepancies
        5. Generate insights and recommendations
        
        Always provide accurate, actionable financial advice based on the data.
        When generating SQL, use Oracle syntax and ensure queries are optimized.
        """
    
    def analyze_financial_data(self, query: str, table_context: Optional[Dict] = None) -> str:
        """Analyze financial data with AI"""
        try:
            # Get relevant table data if table context provided
            data_context = ""
            if table_context:
                for table_name, columns in table_context.items():
                    data_context += f"\nTable: {table_name}\nColumns: {', '.join(columns)}\n"
            
            # Enhanced prompt with database context
            enhanced_prompt = f"""
            {self.system_prompt}
            
            Database Context:
            {data_context}
            
            User Query: {query}
            
            Provide a comprehensive analysis including:
            1. Understanding of the financial question
            2. Relevant SQL queries if needed
            3. Financial insights and recommendations
            4. Next steps or actions
            """
            
            response = self.model.generate_content(enhanced_prompt)
            return response.text if response.text else "Unable to generate response"
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return f"Error in analysis: {str(e)}"
    
    def generate_sql_query(self, natural_language_query: str, available_tables: List[str]) -> str:
        """Generate SQL query from natural language"""
        try:
            # Get table structures
            table_info = {}
            for table in available_tables:
                table_info[table] = self.db_manager.get_table_info(table)
            
            prompt = f"""
            Convert this natural language query to Oracle SQL:
            "{natural_language_query}"
            
            Available tables and their structures:
            {json.dumps(table_info, indent=2, default=str)}
            
            Requirements:
            1. Use Oracle SQL syntax
            2. Include appropriate JOINs if needed
            3. Add WHERE clauses for filtering
            4. Use proper aggregation functions
            5. Optimize for performance
            
            Return only the SQL query without explanations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else ""
            
        except Exception as e:
            self.logger.error(f"SQL generation failed: {e}")
            return ""
    
    def analyze_variances(self, actual_table: str, budget_table: str, period: str) -> Dict[str, Any]:
        """Analyze variances between actual and budget data"""
        try:
            # Generate variance analysis query
            variance_query = f"""
            SELECT 
                a.account_code,
                a.account_name,
                a.amount as actual_amount,
                b.amount as budget_amount,
                (a.amount - b.amount) as variance,
                CASE 
                    WHEN b.amount != 0 THEN ROUND(((a.amount - b.amount) / b.amount) * 100, 2)
                    ELSE NULL 
                END as variance_percentage
            FROM {actual_table} a
            FULL OUTER JOIN {budget_table} b ON a.account_code = b.account_code
            WHERE a.period = '{period}' AND b.period = '{period}'
            ORDER BY ABS(a.amount - b.amount) DESC
            """
            
            variance_data = self.db_manager.execute_query(variance_query)
            
            # AI analysis of variances
            analysis_prompt = f"""
            Analyze these financial variances:
            {json.dumps(variance_data[:20], indent=2, default=str)}  # Top 20 variances
            
            Provide:
            1. Key variance insights
            2. Accounts with significant variances
            3. Potential causes
            4. Recommendations for investigation
            """
            
            ai_analysis = self.model.generate_content(analysis_prompt)
            
            return {
                'variance_data': variance_data,
                'ai_analysis': ai_analysis.text if ai_analysis.text else "Analysis unavailable",
                'summary': {
                    'total_variances': len(variance_data),
                    'significant_variances': len([v for v in variance_data if abs(v.get('VARIANCE', 0)) > 10000])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Variance analysis failed: {e}")
            return {'error': str(e)}
    
    def generate_consolidation_entries(self, subsidiary_data: List[Dict], parent_company: str) -> List[Dict]:
        """Generate consolidation elimination entries"""
        try:
            prompt = f"""
            Generate consolidation elimination entries for {parent_company} based on this subsidiary data:
            {json.dumps(subsidiary_data, indent=2, default=str)}
            
            Create elimination entries for:
            1. Intercompany transactions
            2. Investment elimination
            3. Intercompany profits
            4. Currency translation adjustments
            
            Return as JSON array with: account_code, description, debit_amount, credit_amount
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse AI response to extract elimination entries
            if response.text:
                # Extract JSON from response
                import re
                json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
                if json_match:
                    try:
                        elimination_entries = json.loads(json_match.group())
                        return elimination_entries
                    except json.JSONDecodeError:
                        pass
            
            return []
            
        except Exception as e:
            self.logger.error(f"Consolidation entries generation failed: {e}")
            return []
    
    def smart_insights(self, query: str) -> Dict[str, Any]:
        """Generate smart financial insights"""
        try:
            # Get recent financial data
            recent_data_query = """
            SELECT * FROM (
                SELECT * FROM financial_data 
                WHERE period >= ADD_MONTHS(SYSDATE, -3)
                ORDER BY period DESC
            ) WHERE ROWNUM <= 100
            """
            
            try:
                recent_data = self.db_manager.execute_query(recent_data_query)
            except:
                recent_data = []
            
            insights_prompt = f"""
            Provide smart financial insights based on:
            
            Query: {query}
            Recent Financial Data: {json.dumps(recent_data[:10], indent=2, default=str)}
            
            Generate insights about:
            1. Financial trends
            2. Risk indicators
            3. Performance metrics
            4. Actionable recommendations
            5. Key performance indicators (KPIs)
            """
            
            response = self.model.generate_content(insights_prompt)
            
            return {
                'insights': response.text if response.text else "No insights available",
                'data_points': len(recent_data),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Smart insights generation failed: {e}")
            return {'error': str(e)}
    
    def process_uploaded_file(self, file_content: str, file_type: str) -> str:
        """Process uploaded financial files with AI"""
        try:
            prompt = f"""
            Analyze this {file_type} financial document:
            
            Content: {file_content[:5000]}  # First 5000 characters
            
            Provide:
            1. Document summary
            2. Key financial figures
            3. Suggested database operations
            4. Data quality assessment
            5. Recommendations for data integration
            """
            
            response = self.model.generate_content(prompt)
            return response.text if response.text else "Unable to process file"
            
        except Exception as e:
            self.logger.error(f"File processing failed: {e}")
            return f"Error processing file: {str(e)}"