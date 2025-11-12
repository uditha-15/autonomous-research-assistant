# Autonomous Multi-Agent AI Research Assistant

An autonomous multi-agent AI research assistant that investigates emerging scientific domains and produces complete Markdown-format research reports—fully autonomously.

## Architecture & Tooling

- **Langchain**: Agent orchestration and workflow management
- **Google Gemini API** (via langchain-google-genai): All LLM-based tasks, planning, and reasoning
- **Beautiful Soup**: Web scraping and parsing
- **Chroma**: Vector database for agent memory, semantic storage, and fast retrieval

## Features

- **Autonomous Workflow**: Runs from topic selection to report output without human intervention
- **Multi-Agent System**: Specialized agents (Researcher, Planner, Data Alchemist, Experimenter, Reviewer, Critic) collaborate via shared Chroma memory
- **Web Scraping**: Extracts scientific articles, papers, and data tables from the web
- **Semantic Memory**: All findings stored in Chroma for persistent agent memory and retrieval
- **Self-Critique**: Agents validate and improve each research stage iteratively
- **Data Visualization**: Generates plots and visualizations for key results
- **Comprehensive Reports**: Markdown-format reports with metadata, sections, plots, citations, and confidence assessments

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Usage

### Web Interface (Recommended for Render)

Start the Flask web server:

```bash
python app.py
```

Then visit `http://localhost:5000` in your browser.

### Command Line

```python
from research_assistant import AutonomousResearchAssistant

assistant = AutonomousResearchAssistant()
report = assistant.run_autonomous_research()
print(report)
```

Or run directly:

```bash
python main.py
```

Or with a specific domain:

```bash
python main.py "Quantum Computing"
```

## Workflow

1. **Identify Trending Domain**: Performs web search to select a current, relevant scientific field
2. **Generate Research Questions**: Brainstorms and refines questions and hypotheses
3. **Scrape & Process Data**: Extracts scientific articles, papers, and data tables from the web
4. **Embed and Store Knowledge**: Adds all relevant documents to Chroma for persistent memory
5. **Collaborate & Self-Critique**: Orchestrates agents to iterate, validate, and improve each stage
6. **Analyze & Visualize Data**: Prepares and visualizes key results
7. **Generate Final Report**: Compiles all findings into a Markdown document

## Agent Roles

- **Researcher**: Conducts web searches and gathers information
- **Planner**: Generates research questions and plans investigation strategy
- **Data Alchemist**: Processes and cleans scraped data
- **Experimenter**: Designs and runs experiments/analyses
- **Reviewer**: Reviews findings and ensures quality
- **Critic**: Provides critical feedback and suggests improvements

## Output

The system generates a comprehensive Markdown report including:
- Topic overview and research questions
- Data sources and methodology
- Experimental results and analyses
- Visualizations and plots
- Citations and references
- Confidence assessments
- Agent decision logs and critiques

## Deployment to Render

This application is ready to deploy on Render. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy Steps:

1. Push code to GitHub
2. Connect to Render
3. Set environment variable: `GOOGLE_API_KEY`
4. Deploy!

The app includes:
- Flask web interface
- REST API endpoints
- Background task processing
- Automatic report generation

## API Endpoints

- `GET /` - Web interface
- `GET /api/health` - Health check
- `POST /api/research/start` - Start research task
- `GET /api/research/status/<task_id>` - Get task status
- `GET /api/research/report/<task_id>` - Download report
- `GET /api/research/list` - List all tasks

## License

MIT

# autonomous-research-assistant
