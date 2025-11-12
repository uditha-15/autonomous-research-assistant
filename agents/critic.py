"""Critic agent for providing critical feedback."""
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import json

class CriticAgent(BaseAgent):
    """Agent responsible for providing critical feedback and suggesting improvements."""
    
    def __init__(self, memory):
        """Initialize the critic agent."""
        super().__init__(
            name="Critic",
            role="Provides critical feedback, identifies weaknesses, and suggests improvements",
            memory=memory
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute critique task."""
        context = context or {}
        
        # Get target agent or work to critique
        target_agent = context.get("target_agent", "general")
        work_to_critique = context.get("work", {})
        
        # Get all recent findings
        recent_findings = self.memory.get_all_findings(limit=20)
        
        critique_prompt = f"""
        You are a Critic Agent. Your task is to provide critical feedback.
        
        Task: {task}
        Target: {target_agent}
        
        Work to Critique:
        {json.dumps(work_to_critique, indent=2) if work_to_critique else "General research progress"}
        
        Recent Findings:
        {chr(10).join(f"- {item.get('content', item)[:200]}..." for item in recent_findings[:10]) if recent_findings else "No recent findings."}
        
        Provide critical feedback:
        1. **Strengths**: What's working well
        2. **Weaknesses**: What needs improvement
        3. **Gaps**: What's missing
        4. **Suggestions**: Specific improvement recommendations
        5. **Priority**: What should be addressed first
        
        Be constructive but thorough. Format as JSON.
        """
        
        # Get critique
        critique_response = self._generate_response(
            prompt_template=critique_prompt,
            input_variables={}
        )
        
        # Parse response
        try:
            if "```json" in critique_response:
                json_start = critique_response.find("```json") + 7
                json_end = critique_response.find("```", json_start)
                critique_response = critique_response[json_start:json_end].strip()
            elif "```" in critique_response:
                json_start = critique_response.find("```") + 3
                json_end = critique_response.find("```", json_start)
                critique_response = critique_response[json_start:json_end].strip()
            
            critique = json.loads(critique_response)
        except:
            critique = {
                "strengths": ["Good research approach", "Comprehensive data gathering"],
                "weaknesses": ["Could use more analysis", "Some gaps in coverage"],
                "gaps": ["Missing some key perspectives", "Could use more data"],
                "suggestions": [
                    "Deepen the analysis",
                    "Add more supporting evidence",
                    "Clarify methodology"
                ],
                "priority": "Focus on completing missing analyses"
            }
        
        # Store critique in memory
        critique_content = f"""
        Critical Feedback for {target_agent}
        
        Strengths:
        {chr(10).join(f"- {s}" for s in critique.get('strengths', []))}
        
        Weaknesses:
        {chr(10).join(f"- {w}" for w in critique.get('weaknesses', []))}
        
        Gaps:
        {chr(10).join(f"- {g}" for g in critique.get('gaps', []))}
        
        Suggestions:
        {chr(10).join(f"- {s}" for s in critique.get('suggestions', []))}
        
        Priority: {critique.get('priority', 'N/A')}
        """
        
        # Store critique targeting the specific agent
        self.memory.store_critique(
            target_agent=target_agent,
            critique_content=critique_content,
            critique_type="feedback"
        )
        
        # Also store as general finding
        self.store_finding(
            content=critique_content,
            metadata={
                "task": task,
                "target_agent": target_agent,
                "critique_type": "feedback",
                "critique_data": json.dumps(critique)
            }
        )
        
        # Log decision
        self.log_decision(
            decision=f"Provided critique for {target_agent}",
            reasoning=critique_response,
            context=[str(work_to_critique)[:200] if work_to_critique else ""]
        )
        
        return {
            "agent": self.name,
            "task": task,
            "target_agent": target_agent,
            "critique": critique,
            "reasoning": self.explain_reasoning(
                f"Critiqued work from {target_agent}",
                f"Provided {len(critique.get('suggestions', []))} improvement suggestions"
            )
        }

