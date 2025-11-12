"""Main research assistant orchestrator."""
from typing import Dict, List, Any, Optional
from memory import ResearchMemory
from agents import (
    ResearcherAgent, PlannerAgent, DataAlchemistAgent,
    ExperimenterAgent, ReviewerAgent, CriticAgent
)
from web_scraper import WebScraper
from config import Config
import os
from datetime import datetime
import json

class AutonomousResearchAssistant:
    """Main orchestrator for autonomous research."""
    
    def __init__(self):
        """Initialize the research assistant."""
        Config.validate()
        
        # Initialize memory
        self.memory = ResearchMemory()
        
        # Initialize agents
        self.researcher = ResearcherAgent(self.memory)
        self.planner = PlannerAgent(self.memory)
        self.data_alchemist = DataAlchemistAgent(self.memory)
        self.experimenter = ExperimenterAgent(self.memory)
        self.reviewer = ReviewerAgent(self.memory)
        self.critic = CriticAgent(self.memory)
        
        # Initialize web scraper
        self.scraper = WebScraper()
        
        # Workflow log
        self.workflow_log: List[Dict[str, Any]] = []
        
        # Create output directories
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        os.makedirs(Config.VISUALIZATIONS_DIR, exist_ok=True)
    
    def identify_trending_domain(self) -> str:
        """Step 1: Identify a trending scientific domain."""
        self._log_workflow_step("identify_domain", "Starting domain identification")
        
        # Use LLM to identify trending domain
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            temperature=Config.TEMPERATURE,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        prompt = """
        Identify a current, trending scientific domain or research topic that would be interesting to investigate.
        Choose something that:
        1. Is currently active in research
        2. Has recent developments
        3. Has available data and sources
        4. Is scientifically significant
        
        Provide just the topic name in a single line, no explanation needed.
        Examples: "Quantum Computing Applications", "CRISPR Gene Editing", "Large Language Models", etc.
        """
        
        response = llm.invoke(prompt)
        domain = response.content.strip() if hasattr(response, 'content') else str(response).strip()
        
        self._log_workflow_step("identify_domain", f"Identified domain: {domain}")
        self.memory.store_document(
            content=f"Research Domain Selected: {domain}",
            metadata={"step": "domain_selection", "timestamp": datetime.now().isoformat()},
            agent_name="Orchestrator",
            document_type="workflow_step"
        )
        
        return domain
    
    def generate_research_questions(self, domain: str) -> Dict[str, Any]:
        """Step 2: Generate research questions."""
        self._log_workflow_step("generate_questions", f"Generating questions for: {domain}")
        
        # Use Planner agent
        plan_result = self.planner.execute(
            task=f"Create a comprehensive research plan for: {domain}",
            context={"domain": domain}
        )
        
        self._log_workflow_step("generate_questions", "Research plan generated", plan_result)
        return plan_result
    
    def scrape_and_process_data(self, domain: str, research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Scrape and process data."""
        self._log_workflow_step("scrape_data", f"Scraping data for: {domain}")
        
        # Use Researcher agent
        research_result = self.researcher.execute(
            task=f"Gather information about: {domain}",
            context={"domain": domain, "research_plan": research_plan}
        )
        
        # Process scraped data with Data Alchemist
        processed_result = self.data_alchemist.execute(
            task=f"Process data related to: {domain}",
            context={
                "data": research_result.get("findings", {}).get("key_findings", []),
                "tables": []
            }
        )
        
        self._log_workflow_step("scrape_data", "Data scraped and processed", {
            "research": research_result,
            "processed": processed_result
        })
        
        return {
            "research": research_result,
            "processed": processed_result
        }
    
    def analyze_and_experiment(self, domain: str, data: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Analyze data and run experiments."""
        self._log_workflow_step("analyze", f"Analyzing data for: {domain}")
        
        # Use Experimenter agent
        experiment_result = self.experimenter.execute(
            task=f"Design and run experiments for: {domain}",
            context={
                "domain": domain,
                "research_plan": plan,
                "processed_data": data.get("processed", {})
            }
        )
        
        self._log_workflow_step("analyze", "Experiments completed", experiment_result)
        return experiment_result
    
    def review_and_critique(self, domain: str, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Review findings and get critiques."""
        self._log_workflow_step("review", f"Reviewing findings for: {domain}")
        
        # Get all findings
        all_findings = self.memory.get_all_findings(limit=100)
        
        # Use Reviewer agent
        review_result = self.reviewer.execute(
            task=f"Review all research findings for: {domain}",
            context={"findings": all_findings}
        )
        
        # Use Critic agent for each major component
        critiques = {}
        for agent_name in ["Researcher", "Planner", "DataAlchemist", "Experimenter"]:
            critique_result = self.critic.execute(
                task=f"Critique the work of {agent_name}",
                context={
                    "target_agent": agent_name,
                    "work": all_results
                }
            )
            critiques[agent_name] = critique_result
        
        self._log_workflow_step("review", "Review and critique completed", {
            "review": review_result,
            "critiques": critiques
        })
        
        return {
            "review": review_result,
            "critiques": critiques
        }
    
    def generate_visualizations(self, results: Dict[str, Any]) -> List[str]:
        """Step 6: Generate visualizations."""
        self._log_workflow_step("visualize", "Generating visualizations")
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        
        visualization_paths = []
        
        # Create a simple summary visualization
        try:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            # Agent activity chart
            agent_names = ["Researcher", "Planner", "DataAlchemist", "Experimenter", "Reviewer", "Critic"]
            activity_counts = [
                len([f for f in self.memory.get_agent_context(agent, limit=100)])
                for agent in agent_names
            ]
            
            axes[0].bar(agent_names, activity_counts)
            axes[0].set_title("Agent Activity")
            axes[0].set_ylabel("Number of Findings")
            axes[0].tick_params(axis='x', rotation=45)
            
            # Quality metrics (if available)
            if "review" in results and "quality_metrics" in results["review"]:
                metrics = results["review"]["quality_metrics"]
                metric_names = list(metrics.keys())[:5]
                metric_values = [metrics.get(m, 0) for m in metric_names]
                
                axes[1].barh(metric_names, metric_values)
                axes[1].set_title("Quality Metrics")
            
            plt.tight_layout()
            viz_path = os.path.join(Config.VISUALIZATIONS_DIR, f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(viz_path)
            plt.close()
            
            visualization_paths.append(viz_path)
        except Exception as e:
            print(f"Error creating visualization: {e}")
        
        self._log_workflow_step("visualize", f"Generated {len(visualization_paths)} visualizations")
        return visualization_paths
    
    def generate_report(self, 
                       domain: str,
                       plan: Dict[str, Any],
                       data_results: Dict[str, Any],
                       experiment_results: Dict[str, Any],
                       review_results: Dict[str, Any],
                       visualizations: List[str]) -> str:
        """Step 7: Generate final Markdown report."""
        self._log_workflow_step("generate_report", "Generating final report")
        
        # Get all findings and logs
        all_findings = self.memory.get_all_findings(limit=200)
        all_decisions = []
        for agent in [self.researcher, self.planner, self.data_alchemist, 
                     self.experimenter, self.reviewer, self.critic]:
            all_decisions.extend(agent.decision_log)
        
        # Build report
        report_lines = []
        
        # Header
        report_lines.append("# Autonomous Research Report")
        report_lines.append("")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Research Domain:** {domain}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("## Executive Summary")
        report_lines.append("")
        report_lines.append("This report was generated autonomously by a multi-agent AI research system.")
        report_lines.append("The system investigated the selected domain using specialized agents that")
        report_lines.append("collaborated through shared memory and iterative refinement.")
        report_lines.append("")
        
        # Research Questions
        report_lines.append("## Research Questions")
        report_lines.append("")
        if "plan" in plan and "research_questions" in plan["plan"]:
            for i, question in enumerate(plan["plan"]["research_questions"], 1):
                report_lines.append(f"{i}. {question}")
        report_lines.append("")
        
        # Hypotheses
        report_lines.append("## Hypotheses")
        report_lines.append("")
        if "plan" in plan and "hypotheses" in plan["plan"]:
            for i, hypothesis in enumerate(plan["plan"]["hypotheses"], 1):
                report_lines.append(f"{i}. {hypothesis}")
        report_lines.append("")
        
        # Methodology
        report_lines.append("## Methodology")
        report_lines.append("")
        report_lines.append("### Investigation Strategy")
        if "plan" in plan and "investigation_strategy" in plan["plan"]:
            for i, step in enumerate(plan["plan"]["investigation_strategy"], 1):
                report_lines.append(f"{i}. {step}")
        report_lines.append("")
        
        # Key Findings
        report_lines.append("## Key Findings")
        report_lines.append("")
        for i, finding in enumerate(all_findings[:20], 1):
            content = finding.get("content", str(finding))[:500]
            report_lines.append(f"### Finding {i}")
            report_lines.append("")
            report_lines.append(content)
            report_lines.append("")
            if finding.get("metadata", {}).get("agent_name"):
                report_lines.append(f"*Source: {finding['metadata']['agent_name']}*")
            report_lines.append("")
        
        # Experimental Results
        report_lines.append("## Experimental Results")
        report_lines.append("")
        if "results" in experiment_results:
            for result in experiment_results["results"]:
                report_lines.append(f"### {result.get('experiment_name', 'Experiment')}")
                report_lines.append("")
                report_lines.append(f"**Methodology:** {result.get('methodology', 'N/A')}")
                report_lines.append("")
                report_lines.append("**Results:**")
                if "key_findings" in result.get("results", {}):
                    for finding in result["results"]["key_findings"]:
                        report_lines.append(f"- {finding}")
                report_lines.append("")
                report_lines.append(f"**Interpretation:** {result.get('interpretation', 'N/A')}")
                report_lines.append("")
        
        # Review and Quality Assessment
        report_lines.append("## Quality Assessment")
        report_lines.append("")
        if "review" in review_results:
            review = review_results["review"]
            report_lines.append(f"**Quality Score:** {review.get('quality_score', 'N/A')}")
            report_lines.append(f"**Completeness:** {review.get('completeness', 'N/A')}")
            report_lines.append(f"**Accuracy:** {review.get('accuracy', 'N/A')}")
            report_lines.append(f"**Coherence:** {review.get('coherence', 'N/A')}")
            report_lines.append("")
            report_lines.append("**Recommendations:**")
            for rec in review.get("recommendations", []):
                report_lines.append(f"- {rec}")
            report_lines.append("")
        
        # Critiques
        report_lines.append("## Critical Feedback")
        report_lines.append("")
        if "critiques" in review_results:
            for agent_name, critique_data in review_results["critiques"].items():
                report_lines.append(f"### Feedback for {agent_name}")
                report_lines.append("")
                critique = critique_data.get("critique", {})
                report_lines.append("**Strengths:**")
                for strength in critique.get("strengths", []):
                    report_lines.append(f"- {strength}")
                report_lines.append("")
                report_lines.append("**Suggestions:**")
                for suggestion in critique.get("suggestions", []):
                    report_lines.append(f"- {suggestion}")
                report_lines.append("")
        
        # Visualizations
        if visualizations:
            report_lines.append("## Visualizations")
            report_lines.append("")
            for viz_path in visualizations:
                viz_name = os.path.basename(viz_path)
                report_lines.append(f"![Visualization]({viz_path})")
                report_lines.append("")
        
        # Agent Decision Logs
        report_lines.append("## Agent Decision Logs")
        report_lines.append("")
        report_lines.append("This section documents key decisions made by each agent during the research process.")
        report_lines.append("")
        for decision in all_decisions[:30]:  # Limit to 30 most recent
            report_lines.append(f"### {decision.get('agent', 'Unknown')} - {decision.get('timestamp', 'Unknown')}")
            report_lines.append("")
            report_lines.append(f"**Decision:** {decision.get('decision', 'N/A')}")
            report_lines.append("")
            report_lines.append(f"**Reasoning:** {decision.get('reasoning', 'N/A')[:500]}")
            report_lines.append("")
        
        # Citations and References
        report_lines.append("## Citations and References")
        report_lines.append("")
        report_lines.append("All findings were generated through autonomous research using:")
        report_lines.append("- Google Gemini API for LLM capabilities")
        report_lines.append("- Chroma vector database for memory and retrieval")
        report_lines.append("- Beautiful Soup for web scraping")
        report_lines.append("- LangChain for agent orchestration")
        report_lines.append("")
        
        # Confidence Assessment
        report_lines.append("## Confidence Assessment")
        report_lines.append("")
        confidence_score = review_results.get("review", {}).get("quality_metrics", {}).get("quality_score", "Good")
        report_lines.append(f"**Overall Confidence:** {confidence_score}")
        report_lines.append("")
        report_lines.append("This autonomous research was conducted with the following confidence levels:")
        report_lines.append("- Data Collection: High")
        report_lines.append("- Analysis: Medium-High")
        report_lines.append("- Synthesis: Medium-High")
        report_lines.append("")
        report_lines.append("Note: This is an autonomous system and results should be validated by human experts.")
        report_lines.append("")
        
        # Workflow Summary
        report_lines.append("## Workflow Summary")
        report_lines.append("")
        report_lines.append("The research followed these steps:")
        for step in self.workflow_log:
            report_lines.append(f"- **{step.get('step', 'Unknown')}**: {step.get('description', 'N/A')}")
        report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # Save report
        report_path = os.path.join(
            Config.REPORTS_DIR,
            f"research_report_{domain.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self._log_workflow_step("generate_report", f"Report saved to: {report_path}")
        return report_content
    
    def _log_workflow_step(self, step: str, description: str, data: Optional[Dict[str, Any]] = None):
        """Log a workflow step."""
        log_entry = {
            "step": step,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.workflow_log.append(log_entry)
        print(f"[{step}] {description}")
    
    def run_autonomous_research(self, domain: Optional[str] = None) -> str:
        """Run the complete autonomous research workflow."""
        print("=" * 60)
        print("Starting Autonomous Research Workflow")
        print("=" * 60)
        print()
        
        try:
            # Step 1: Identify domain
            if not domain:
                domain = self.identify_trending_domain()
            print(f"Selected Domain: {domain}")
            print()
            
            # Step 2: Generate research questions
            print("Step 2: Generating research questions...")
            plan_result = self.generate_research_questions(domain)
            print()
            
            # Step 3: Scrape and process data
            print("Step 3: Scraping and processing data...")
            data_results = self.scrape_and_process_data(domain, plan_result)
            print()
            
            # Step 4: Analyze and experiment
            print("Step 4: Analyzing data and running experiments...")
            experiment_results = self.analyze_and_experiment(domain, data_results, plan_result)
            print()
            
            # Step 5: Review and critique
            print("Step 5: Reviewing findings and getting critiques...")
            all_results = {
                "plan": plan_result,
                "data": data_results,
                "experiments": experiment_results
            }
            review_results = self.review_and_critique(domain, all_results)
            print()
            
            # Step 6: Generate visualizations
            print("Step 6: Generating visualizations...")
            visualizations = self.generate_visualizations({
                "experiments": experiment_results,
                "review": review_results
            })
            print()
            
            # Step 7: Generate final report
            print("Step 7: Generating final report...")
            report = self.generate_report(
                domain=domain,
                plan=plan_result,
                data_results=data_results,
                experiment_results=experiment_results,
                review_results=review_results,
                visualizations=visualizations
            )
            print()
            
            print("=" * 60)
            print("Research Complete!")
            print("=" * 60)
            print(f"Report generated with {len(self.workflow_log)} workflow steps")
            print(f"Total findings stored: {len(self.memory.get_all_findings(limit=1000))}")
            
            return report
            
        except Exception as e:
            error_msg = f"Error in autonomous research: {str(e)}"
            print(error_msg)
            self._log_workflow_step("error", error_msg)
            raise

