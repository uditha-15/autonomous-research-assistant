"""Researcher agent for gathering information."""
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
from web_scraper import WebScraper
import json

class ResearcherAgent(BaseAgent):
    """Agent responsible for conducting research and gathering information."""
    
    def __init__(self, memory):
        """Initialize the researcher agent."""
        super().__init__(
            name="Researcher",
            role="Conducts web searches and gathers scientific information from various sources",
            memory=memory
        )
        self.scraper = WebScraper()
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute research task."""
        context = context or {}
        
        # Get relevant context from memory
        relevant_context = self.get_context(task, limit=5)
        
        # Build research prompt
        context_summary = "\n".join([
            f"- {item['content'][:200]}..." 
            for item in relevant_context[:3]
        ])
        
        research_prompt = f"""
        You are a Research Agent. Your task is to: {task}
        
        Previous findings in this research:
        {context_summary if context_summary else "No previous findings."}
        
        Based on the task and previous context, identify:
        1. What specific information needs to be gathered
        2. What types of sources would be most valuable (research papers, articles, data repositories, etc.)
        3. Key search terms and queries to use
        4. Specific URLs or sources to investigate (if any were provided)
        
        Provide your research plan in JSON format with:
        - search_queries: List of search queries
        - source_types: Types of sources to prioritize
        - key_terms: Important terms to focus on
        - research_questions: Specific questions to answer
        """
        
        # Get research plan from LLM
        plan_response = self._generate_response(
            prompt_template=research_prompt,
            input_variables={}
        )
        
        # Try to parse JSON from response
        try:
            # Extract JSON from response if it's wrapped in markdown
            if "```json" in plan_response:
                json_start = plan_response.find("```json") + 7
                json_end = plan_response.find("```", json_start)
                plan_response = plan_response[json_start:json_end].strip()
            elif "```" in plan_response:
                json_start = plan_response.find("```") + 3
                json_end = plan_response.find("```", json_start)
                plan_response = plan_response[json_start:json_end].strip()
            
            plan = json.loads(plan_response)
        except:
            # Fallback: create a simple plan
            plan = {
                "search_queries": [task],
                "source_types": ["research papers", "articles", "data repositories"],
                "key_terms": task.split(),
                "research_questions": [task]
            }
        
        # Log decision
        self.log_decision(
            decision=f"Created research plan for: {task}",
            reasoning=plan_response,
            context=[item['content'][:100] for item in relevant_context[:3]]
        )
        
        # Simulate research findings (in production, this would use actual search APIs)
        findings = {
            "plan": plan,
            "sources_found": [],
            "key_findings": [],
            "recommendations": []
        }
        
        # Generate synthetic findings based on the plan
        findings_prompt = f"""
        Based on the research plan:
        {json.dumps(plan, indent=2)}
        
        Generate a summary of what information would typically be found for this research topic.
        Include:
        1. Key findings that would be discovered
        2. Important sources that would be relevant
        3. Data points or statistics that might be found
        4. Gaps in current knowledge
        
        Format as a structured research summary.
        """
        
        findings_summary = self._generate_response(
            prompt_template=findings_prompt,
            input_variables={}
        )
        
        findings["key_findings"] = [findings_summary]
        
        # Store findings
        self.store_finding(
            content=findings_summary,
            metadata={
                "task": task,
                "plan": json.dumps(plan),
                "findings_type": "research_summary"
            }
        )
        
        return {
            "agent": self.name,
            "task": task,
            "plan": plan,
            "findings": findings,
            "reasoning": self.explain_reasoning(
                f"Researched topic: {task}",
                f"Generated research plan and findings summary"
            )
        }

