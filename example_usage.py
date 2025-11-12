"""Example usage of the autonomous research assistant."""
from research_assistant import AutonomousResearchAssistant
from config import Config

def example_basic_usage():
    """Basic usage example."""
    print("Example 1: Basic Autonomous Research")
    print("-" * 60)
    
    assistant = AutonomousResearchAssistant()
    
    # Run with auto-selected domain
    report = assistant.run_autonomous_research()
    
    print(f"\nReport length: {len(report)} characters")
    print(f"Report preview:\n{report[:500]}...")

def example_specific_domain():
    """Example with a specific domain."""
    print("\nExample 2: Research on Specific Domain")
    print("-" * 60)
    
    assistant = AutonomousResearchAssistant()
    
    # Run with specific domain
    domain = "Quantum Machine Learning"
    report = assistant.run_autonomous_research(domain=domain)
    
    print(f"\nResearch completed on: {domain}")
    print(f"Report saved in: {Config.REPORTS_DIR}/")

def example_agent_interaction():
    """Example of interacting with individual agents."""
    print("\nExample 3: Direct Agent Interaction")
    print("-" * 60)
    
    from memory import ResearchMemory
    
    memory = ResearchMemory()
    
    # Create individual agents
    from agents import PlannerAgent, ResearcherAgent
    
    planner = PlannerAgent(memory)
    researcher = ResearcherAgent(memory)
    
    # Use planner
    domain = "CRISPR Gene Editing"
    plan_result = planner.execute(
        task=f"Create research plan for: {domain}",
        context={"domain": domain}
    )
    
    print(f"Plan generated: {plan_result.get('plan', {}).get('research_questions', [])}")
    
    # Use researcher
    research_result = researcher.execute(
        task=f"Gather information about: {domain}",
        context={"domain": domain}
    )
    
    print(f"Research findings: {len(research_result.get('findings', {}).get('key_findings', []))} findings")

if __name__ == "__main__":
    # Uncomment the example you want to run
    
    # example_basic_usage()
    # example_specific_domain()
    example_agent_interaction()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

