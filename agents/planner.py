"""Planner agent for generating research questions and strategy."""
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import json

class PlannerAgent(BaseAgent):
    """Agent responsible for planning research strategy and generating questions."""
    
    def __init__(self, memory):
        """Initialize the planner agent."""
        super().__init__(
            name="Planner",
            role="Generates research questions, hypotheses, and investigation strategy",
            memory=memory
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute planning task."""
        context = context or {}
        
        # Get relevant context
        relevant_context = self.get_context(task, limit=10)
        
        # Get previous research findings
        research_findings = [
            item for item in relevant_context 
            if item.get('metadata', {}).get('agent_name') == 'Researcher'
        ]
        
        # Build planning prompt
        findings_summary = "\n".join([
            f"- {item['content'][:300]}..." 
            for item in research_findings[:5]
        ])
        
        planning_prompt = f"""
        You are a Research Planner Agent. Your task is to create a comprehensive research plan.
        
        Research Topic/Goal: {task}
        
        Previous Research Findings:
        {findings_summary if findings_summary else "No previous findings available."}
        
        Based on the topic and findings, generate:
        1. **Research Questions**: 3-5 specific, answerable research questions
        2. **Hypotheses**: 2-3 testable hypotheses related to the topic
        3. **Investigation Strategy**: Step-by-step plan for investigating the topic
        4. **Data Requirements**: What data or information is needed
        5. **Success Criteria**: How to measure if the research is successful
        
        Provide your response in JSON format with these keys:
        - research_questions: List of questions
        - hypotheses: List of hypotheses
        - investigation_strategy: List of steps
        - data_requirements: List of requirements
        - success_criteria: List of criteria
        """
        
        # Get plan from LLM
        plan_response = self._generate_response(
            prompt_template=planning_prompt,
            input_variables={}
        )
        
        # Parse JSON response
        try:
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
            # Fallback plan
            plan = {
                "research_questions": [
                    f"What are the key aspects of {task}?",
                    f"What are recent developments in {task}?",
                    f"What are the main challenges in {task}?"
                ],
                "hypotheses": [
                    f"{task} has significant recent developments",
                    f"{task} involves multiple interconnected factors"
                ],
                "investigation_strategy": [
                    "Gather background information",
                    "Identify key sources",
                    "Analyze findings",
                    "Synthesize results"
                ],
                "data_requirements": [
                    "Research papers and articles",
                    "Data tables and statistics",
                    "Expert opinions and analyses"
                ],
                "success_criteria": [
                    "Comprehensive understanding of the topic",
                    "Clear answers to research questions",
                    "Well-documented findings"
                ]
            }
        
        # Log decision
        self.log_decision(
            decision=f"Created research plan for: {task}",
            reasoning=plan_response,
            context=[item['content'][:100] for item in research_findings[:3]]
        )
        
        # Store plan
        plan_content = f"""
        Research Plan for: {task}
        
        Research Questions:
        {chr(10).join(f"- {q}" for q in plan.get('research_questions', []))}
        
        Hypotheses:
        {chr(10).join(f"- {h}" for h in plan.get('hypotheses', []))}
        
        Investigation Strategy:
        {chr(10).join(f"{i+1}. {s}" for i, s in enumerate(plan.get('investigation_strategy', [])))}
        """
        
        self.store_finding(
            content=plan_content,
            metadata={
                "task": task,
                "plan_type": "research_plan",
                "plan_data": json.dumps(plan)
            }
        )
        
        return {
            "agent": self.name,
            "task": task,
            "plan": plan,
            "reasoning": self.explain_reasoning(
                f"Planned research strategy for: {task}",
                f"Generated {len(plan.get('research_questions', []))} research questions and investigation strategy"
            )
        }

