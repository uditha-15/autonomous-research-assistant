# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

## Setup (5 minutes)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. **Run your first research:**
   ```bash
   python main.py
   ```

   Or specify a domain:
   ```bash
   python main.py "Quantum Computing"
   ```

## Using in Your Code

```python
from research_assistant import AutonomousResearchAssistant

# Initialize
assistant = AutonomousResearchAssistant()

# Run autonomous research (auto-selects domain)
report = assistant.run_autonomous_research()

# Or specify a domain
report = assistant.run_autonomous_research(domain="CRISPR Gene Editing")

# Report is saved in reports/ directory
# Also returned as string
print(report[:1000])  # Preview
```

## Project Structure

```
autonomous-research-assistant/
├── agents/              # Specialized agent implementations
│   ├── base_agent.py   # Base agent class
│   ├── researcher.py   # Research agent
│   ├── planner.py      # Planning agent
│   ├── data_alchemist.py  # Data processing agent
│   ├── experimenter.py    # Experimentation agent
│   ├── reviewer.py        # Review agent
│   └── critic.py          # Critique agent
├── config.py           # Configuration
├── memory.py           # Chroma vector DB integration
├── web_scraper.py      # Beautiful Soup scraper
├── research_assistant.py  # Main orchestrator
├── main.py             # Entry point
├── example_usage.py    # Usage examples
└── requirements.txt    # Dependencies
```

## How It Works

1. **Domain Selection**: Automatically identifies a trending scientific domain
2. **Planning**: Generates research questions and strategy
3. **Research**: Gathers information from web sources
4. **Data Processing**: Cleans and structures the data
5. **Experimentation**: Runs analyses and experiments
6. **Review**: Quality checks and validation
7. **Critique**: Critical feedback and improvements
8. **Report Generation**: Compiles everything into Markdown

All agents share memory via Chroma vector database, enabling collaboration and context sharing.

## Output

- **Reports**: Saved in `reports/` directory as Markdown files
- **Visualizations**: Saved in `visualizations/` directory as PNG files
- **Memory**: Stored in `.chroma/` directory (vector database)

## Troubleshooting

**Error: GOOGLE_API_KEY not found**
- Make sure you created `.env` file with your API key

**Error: Module not found**
- Run `pip install -r requirements.txt`

**Error: Embedding model issues**
- Check that your Gemini API key has access to embedding models
- The code will try alternative model names automatically

## Next Steps

- Customize agents in `agents/` directory
- Add real search APIs in `web_scraper.py` (currently uses LLM-generated summaries)
- Extend visualization capabilities
- Add more specialized agents

## Notes

- The web scraper currently uses LLM-generated summaries. For production, integrate with:
  - Google Custom Search API
  - arXiv API
  - PubMed API
  - Semantic Scholar API
- All findings are stored in Chroma for persistent memory
- Agents can reference previous work and build upon it

