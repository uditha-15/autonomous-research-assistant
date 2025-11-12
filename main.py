"""Main entry point for the autonomous research assistant."""
import sys
from research_assistant import AutonomousResearchAssistant
from config import Config

def main():
    """Main function to run the research assistant."""
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize assistant
        assistant = AutonomousResearchAssistant()
        
        # Optionally accept domain as command line argument
        domain = None
        if len(sys.argv) > 1:
            domain = " ".join(sys.argv[1:])
            print(f"Using provided domain: {domain}")
        
        # Run autonomous research
        report = assistant.run_autonomous_research(domain=domain)
        
        # Print report preview
        print("\n" + "=" * 60)
        print("REPORT PREVIEW (first 1000 characters)")
        print("=" * 60)
        print(report[:1000])
        print("...")
        print(f"\nFull report saved in {Config.REPORTS_DIR}/")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease create a .env file with your GOOGLE_API_KEY")
        print("You can copy .env.example to .env and add your key.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

