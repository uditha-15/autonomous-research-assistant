"""Base agent class for all specialized agents."""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain.memory import ConversationBufferMemory 
from memory import ResearchMemory
from config import Config
import json
from datetime import datetime

class BaseAgent(ABC):
    """Base class for all research agents."""
    
    def __init__(self, name: str, role: str, memory: ResearchMemory):
        """Initialize the agent."""
        Config.validate()
        
        self.name = name
        self.role = role
        self.memory = memory
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            temperature=Config.TEMPERATURE,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        # Agent-specific memory
        self.agent_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Decision log
        self.decision_log: List[Dict[str, Any]] = []
    
    def get_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant context from shared memory."""
        return self.memory.search_similar(query, n_results=limit)
    
    def store_finding(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store a finding in shared memory."""
        if metadata is None:
            metadata = {}
        
        metadata.update({
            "agent_role": self.role,
            "finding_type": "general"
        })
        
        return self.memory.store_document(
            content=content,
            metadata=metadata,
            agent_name=self.name,
            document_type="finding"
        )
    
    def log_decision(self, decision: str, reasoning: str, context: Optional[List[str]] = None):
        """Log a decision made by the agent."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "decision": decision,
            "reasoning": reasoning,
            "context": context or []
        }
        self.decision_log.append(log_entry)
        
        # Also store in shared memory
        self.memory.store_document(
            content=f"Decision: {decision}\nReasoning: {reasoning}",
            metadata={"log_type": "decision", "context": json.dumps(context or [])},
            agent_name=self.name,
            document_type="decision_log"
        )
    
    def get_previous_findings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get previous findings from this agent."""
        return self.memory.get_agent_context(self.name, limit=limit)
    
    def get_critiques(self) -> List[Dict[str, Any]]:
        """Get critiques for this agent."""
        return self.memory.get_critiques_for_agent(self.name)
    
    @abstractmethod
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the agent's primary task."""
        pass
    
    def _generate_response(self, 
                          prompt_template: str,
                          input_variables: Dict[str, Any],
                          system_message: Optional[str] = None) -> str:
        """Generate a response using the LLM."""
        # Build prompt
        messages = []
        if system_message:
            messages.append(("system", system_message))
        messages.append(("human", prompt_template))
        
        prompt = ChatPromptTemplate.from_messages(messages)
        
        # Format prompt with variables
        formatted_prompt = prompt.format(**input_variables)
        
        # Get response
        response = self.llm.invoke(formatted_prompt)
        
        return response.content if hasattr(response, 'content') else str(response)
    
    def explain_reasoning(self, action: str, result: str) -> str:
        """Generate an explanation of the agent's reasoning."""
        explanation_prompt = f"""
        As the {self.role} agent, explain your reasoning for the following action:
        
        Action: {action}
        Result: {result}
        
        Provide a clear explanation of why you took this action and how it contributes to the research goal.
        """
        
        return self._generate_response(
            prompt_template=explanation_prompt,
            input_variables={}
        )

