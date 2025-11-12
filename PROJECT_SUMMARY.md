# Project Summary

## Overview

This is an **Autonomous Multi-Agent AI Research Assistant** that investigates emerging scientific domains and produces complete Markdown-format research reports—fully autonomously.

## Architecture

### Technology Stack
- **LangChain**: Agent orchestration and workflow management
- **Google Gemini API** (via langchain-google-genai): All LLM tasks
- **Beautiful Soup**: Web scraping and parsing
- **Chroma**: Vector database for agent memory

### Agent System
The system uses 6 specialized agents that collaborate through shared Chroma memory:

1. **Researcher**: Conducts web searches and gathers information
2. **Planner**: Generates research questions and investigation strategy
3. **Data Alchemist**: Processes and cleans scraped data
4. **Experimenter**: Designs and runs experiments/analyses
5. **Reviewer**: Reviews findings and ensures quality
6. **Critic**: Provides critical feedback and improvements

## Key Features

✅ **Fully Autonomous**: Runs from topic selection to report output  
✅ **Multi-Agent Collaboration**: Agents share context via Chroma vector DB  
✅ **Self-Critique**: Agents validate and improve each stage iteratively  
✅ **Comprehensive Reports**: Markdown format with metadata, visualizations, citations  
✅ **Traceable Logs**: All agent decisions and reasoning documented  
✅ **Persistent Memory**: All findings stored in Chroma for future reference  

## Workflow

1. **Identify Trending Domain** → Auto-selects scientific field
2. **Generate Research Questions** → Creates plan and hypotheses
3. **Scrape & Process Data** → Extracts and cleans web data
4. **Embed & Store Knowledge** → Saves to Chroma vector DB
5. **Collaborate & Self-Critique** → Agents iterate and improve
6. **Analyze & Visualize** → Generates plots and analyses
7. **Generate Final Report** → Compiles Markdown report

## File Structure

```
autonomous-research-assistant/
├── agents/                    # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── researcher.py          # Research agent
│   ├── planner.py             # Planning agent
│   ├── data_alchemist.py      # Data processing agent
│   ├── experimenter.py        # Experimentation agent
│   ├── reviewer.py            # Review agent
│   └── critic.py              # Critique agent
├── config.py                  # Configuration management
├── memory.py                  # Chroma vector DB integration
├── web_scraper.py             # Beautiful Soup scraper
├── research_assistant.py      # Main orchestrator
├── main.py                    # Entry point
├── example_usage.py            # Usage examples
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── QUICKSTART.md              # Quick start guide
├── SYSTEM_PROMPT.md           # System prompt for agents
├── .env.example               # Environment template
└── .gitignore                 # Git ignore rules
```

## Usage

### Basic Usage
```bash
python main.py
```

### With Specific Domain
```bash
python main.py "Quantum Machine Learning"
```

### Programmatic Usage
```python
from research_assistant import AutonomousResearchAssistant

assistant = AutonomousResearchAssistant()
report = assistant.run_autonomous_research(domain="CRISPR Gene Editing")
```

## Output

- **Reports**: `reports/` directory (Markdown format)
- **Visualizations**: `visualizations/` directory (PNG images)
- **Memory**: `.chroma/` directory (vector database)

## Requirements

- Python 3.8+
- Google Gemini API key
- All dependencies in `requirements.txt`

## Based On

This implementation is inspired by and adapted from:
- **CAMEL**: Multi-agent communication framework
- **HASHIRU**: Hierarchical agent systems
- **AgentRxiv**: Collaborative autonomous research
- Various LangChain multi-agent examples

## Extensibility

The system is designed to be easily extended:
- Add new agents by inheriting from `BaseAgent`
- Integrate real search APIs in `web_scraper.py`
- Customize agent behavior in individual agent files
- Add new visualization types
- Extend memory capabilities

## Notes

- Web scraping currently uses LLM-generated summaries (can be extended with real APIs)
- All agent reasoning is logged and visible in reports
- Chroma provides persistent memory across sessions
- System is fully autonomous but results should be validated by humans

## License

MIT

