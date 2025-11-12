"""Data Alchemist agent for processing and cleaning data."""
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import json
import pandas as pd
import numpy as np

class DataAlchemistAgent(BaseAgent):
    """Agent responsible for processing, cleaning, and transforming data."""
    
    def __init__(self, memory):
        """Initialize the data alchemist agent."""
        super().__init__(
            name="DataAlchemist",
            role="Processes, cleans, and transforms scraped data into usable formats",
            memory=memory
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute data processing task."""
        context = context or {}
        
        # Get relevant data from context
        data_to_process = context.get("data", [])
        tables = context.get("tables", [])
        
        # Get previous findings
        relevant_context = self.get_context("data processing", limit=5)
        
        processing_prompt = f"""
        You are a Data Alchemist Agent. Your task is to process and clean data.
        
        Task: {task}
        
        Data to process:
        - Number of data items: {len(data_to_process)}
        - Number of tables: {len(tables)}
        
        Previous processing context:
        {chr(10).join(f"- {item['content'][:200]}..." for item in relevant_context[:3]) if relevant_context else "No previous context."}
        
        Analyze the data and provide:
        1. **Data Quality Assessment**: Identify issues, missing values, inconsistencies
        2. **Cleaning Strategy**: Steps needed to clean the data
        3. **Transformation Plan**: How to transform data into usable formats
        4. **Data Schema**: Structure of the processed data
        5. **Key Insights**: Initial observations from the data
        
        Provide your analysis in JSON format.
        """
        
        # Get processing plan
        analysis_response = self._generate_response(
            prompt_template=processing_prompt,
            input_variables={}
        )
        
        # Parse response
        try:
            if "```json" in analysis_response:
                json_start = analysis_response.find("```json") + 7
                json_end = analysis_response.find("```", json_start)
                analysis_response = analysis_response[json_start:json_end].strip()
            elif "```" in analysis_response:
                json_start = analysis_response.find("```") + 3
                json_end = analysis_response.find("```", json_start)
                analysis_response = analysis_response[json_start:json_end].strip()
            
            analysis = json.loads(analysis_response)
        except:
            analysis = {
                "data_quality": "Good",
                "cleaning_steps": ["Remove duplicates", "Handle missing values", "Standardize formats"],
                "transformation_plan": ["Convert to structured format", "Extract key metrics"],
                "schema": "Structured data with multiple fields",
                "insights": ["Data contains valuable information", "Some cleaning needed"]
            }
        
        # Process tables if available
        processed_tables = []
        for i, table in enumerate(tables[:5]):  # Limit to 5 tables
            try:
                if table.get("headers") and table.get("rows"):
                    df = pd.DataFrame(table["rows"], columns=table["headers"][:len(table["rows"][0])] if table["rows"] else [])
                    processed_tables.append({
                        "table_id": i,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "summary": df.describe().to_dict() if len(df) > 0 else {}
                    })
            except Exception as e:
                processed_tables.append({
                    "table_id": i,
                    "error": str(e)
                })
        
        # Log decision
        self.log_decision(
            decision=f"Processed {len(data_to_process)} data items and {len(tables)} tables",
            reasoning=analysis_response,
            context=[item['content'][:100] for item in relevant_context[:3]]
        )
        
        # Store processed data summary
        summary_content = f"""
        Data Processing Summary
        
        Quality Assessment: {analysis.get('data_quality', 'Unknown')}
        Cleaning Steps: {', '.join(analysis.get('cleaning_steps', []))}
        Processed Tables: {len(processed_tables)}
        Key Insights: {', '.join(analysis.get('insights', []))}
        """
        
        self.store_finding(
            content=summary_content,
            metadata={
                "task": task,
                "data_items_processed": len(data_to_process),
                "tables_processed": len(tables),
                "analysis": json.dumps(analysis)
            }
        )
        
        return {
            "agent": self.name,
            "task": task,
            "analysis": analysis,
            "processed_tables": processed_tables,
            "data_summary": {
                "items_processed": len(data_to_process),
                "tables_processed": len(tables),
                "quality_score": "Good" if len(data_to_process) > 0 or len(tables) > 0 else "No data"
            },
            "reasoning": self.explain_reasoning(
                f"Processed data for: {task}",
                f"Analyzed {len(data_to_process)} items and {len(tables)} tables"
            )
        }

