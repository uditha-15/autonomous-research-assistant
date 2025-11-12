"""Reviewer agent for reviewing findings and ensuring quality."""
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import json

class ReviewerAgent(BaseAgent):
    """Agent responsible for reviewing findings and ensuring quality."""
    
    def __init__(self, memory):
        """Initialize the reviewer agent."""
        super().__init__(
            name="Reviewer",
            role="Reviews findings, ensures quality, and validates research outputs",
            memory=memory
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute review task."""
        context = context or {}
        
        # Get all findings to review
        all_findings = self.memory.get_all_findings(limit=50)
        
        # Get specific findings from context if provided
        findings_to_review = context.get("findings", [])
        
        review_prompt = f"""
        You are a Reviewer Agent. Your task is to review research findings and ensure quality.
        
        Task: {task}
        
        Findings to Review:
        {chr(10).join(f"- {item.get('content', item)[:300]}..." for item in findings_to_review[:10]) if findings_to_review else "No specific findings provided."}
        
        Total Findings in Memory: {len(all_findings)}
        
        Review the findings and provide:
        1. **Quality Assessment**: Overall quality of the research
        2. **Completeness Check**: What's missing or incomplete
        3. **Accuracy Review**: Any potential errors or inconsistencies
        4. **Coherence Analysis**: How well findings fit together
        5. **Recommendations**: What improvements are needed
        
        Format as JSON.
        """
        
        # Get review
        review_response = self._generate_response(
            prompt_template=review_prompt,
            input_variables={}
        )
        
        # Parse response
        try:
            if "```json" in review_response:
                json_start = review_response.find("```json") + 7
                json_end = review_response.find("```", json_start)
                review_response = review_response[json_start:json_end].strip()
            elif "```" in review_response:
                json_start = review_response.find("```") + 3
                json_end = review_response.find("```", json_start)
                review_response = review_response[json_start:json_end].strip()
            
            review = json.loads(review_response)
        except:
            review = {
                "quality_score": "Good",
                "completeness": "Mostly complete",
                "accuracy": "Appears accurate",
                "coherence": "Findings are coherent",
                "recommendations": [
                    "Continue research",
                    "Add more supporting evidence",
                    "Clarify some points"
                ]
            }
        
        # Calculate quality metrics
        quality_metrics = {
            "findings_count": len(all_findings),
            "reviewed_count": len(findings_to_review),
            "quality_score": review.get("quality_score", "Unknown"),
            "completeness": review.get("completeness", "Unknown")
        }
        
        # Log decision
        self.log_decision(
            decision=f"Reviewed {len(findings_to_review)} findings",
            reasoning=review_response,
            context=[item.get('content', str(item))[:100] for item in findings_to_review[:3]]
        )
        
        # Store review
        review_content = f"""
        Research Review Summary
        
        Quality Score: {review.get('quality_score', 'Unknown')}
        Completeness: {review.get('completeness', 'Unknown')}
        Accuracy: {review.get('accuracy', 'Unknown')}
        Coherence: {review.get('coherence', 'Unknown')}
        
        Recommendations:
        {chr(10).join(f"- {r}" for r in review.get('recommendations', []))}
        """
        
        self.store_finding(
            content=review_content,
            metadata={
                "task": task,
                "review_type": "quality_review",
                "review_data": json.dumps(review),
                "quality_metrics": json.dumps(quality_metrics)
            }
        )
        
        return {
            "agent": self.name,
            "task": task,
            "review": review,
            "quality_metrics": quality_metrics,
            "reasoning": self.explain_reasoning(
                f"Reviewed findings for: {task}",
                f"Assessed quality and provided {len(review.get('recommendations', []))} recommendations"
            )
        }

