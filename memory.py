"""Chroma vector database integration for agent memory."""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import json
from datetime import datetime
from config import Config

class ResearchMemory:
    """Manages agent memory using Chroma vector database."""
    
    def __init__(self):
        """Initialize the memory system."""
        Config.validate()
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embeddings
        # Note: Google's embedding model name may vary - adjust if needed
        try:
            # Try with explicit model name first
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=Config.GOOGLE_API_KEY
            )
        except Exception as e:
            try:
                # Fallback: try without model name (uses default)
                self.embeddings = GoogleGenerativeAIEmbeddings(
                    google_api_key=Config.GOOGLE_API_KEY
                )
            except Exception as e2:
                # If embeddings fail, we'll use a simple text-based approach
                print(f"Warning: Could not initialize embeddings: {e2}")
                print("Falling back to text-based storage (embeddings disabled)")
                self.embeddings = None
    
    def store_document(self, 
                      content: str, 
                      metadata: Dict[str, Any],
                      agent_name: str,
                      document_type: str = "finding") -> str:
        """Store a document in the vector database."""
        # Create document ID
        doc_id = f"{agent_name}_{document_type}_{datetime.now().isoformat()}"
        
        # Prepare metadata
        full_metadata = {
            **metadata,
            "agent_name": agent_name,
            "document_type": document_type,
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content)
        }
        
        # Generate embedding if available
        if self.embeddings:
            try:
                embedding = self.embeddings.embed_query(content)
                # Store in Chroma with embedding
                self.collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[full_metadata]
                )
            except Exception as e:
                print(f"Warning: Embedding failed, storing without embedding: {e}")
                # Store without embedding
                self.collection.add(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=full_metadata
                )
        else:
            # Store without embedding
            self.collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=full_metadata
            )
        
        return doc_id
    
    def search_similar(self, 
                      query: str, 
                      n_results: int = 5,
                      filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        # If embeddings are available, use semantic search
        if self.embeddings:
            try:
                # Generate query embedding
                query_embedding = self.embeddings.embed_query(query)
                
                # Search
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                    where=filter_metadata
                )
                
                # Format results
                formatted_results = []
                if results['ids'] and len(results['ids'][0]) > 0:
                    for i in range(len(results['ids'][0])):
                        formatted_results.append({
                            "id": results['ids'][0][i],
                            "content": results['documents'][0][i],
                            "metadata": results['metadatas'][0][i],
                            "distance": results['distances'][0][i] if 'distances' in results else None
                        })
                
                return formatted_results
            except Exception as e:
                print(f"Warning: Semantic search failed, using text search: {e}")
        
        # Fallback: text-based search
        all_docs = self.collection.get(limit=100)
        formatted_results = []
        
        if all_docs['ids']:
            # Simple text matching
            query_lower = query.lower()
            for i in range(len(all_docs['ids'])):
                content = all_docs['documents'][i]
                metadata = all_docs['metadatas'][i]
                
                # Check filter
                if filter_metadata:
                    match = all(metadata.get(k) == v for k, v in filter_metadata.items())
                    if not match:
                        continue
                
                # Simple relevance: check if query terms appear in content
                if query_lower in content.lower():
                    formatted_results.append({
                        "id": all_docs['ids'][i],
                        "content": content,
                        "metadata": metadata,
                        "distance": None
                    })
                
                if len(formatted_results) >= n_results:
                    break
        
        return formatted_results
    
    def get_agent_context(self, agent_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent context for a specific agent."""
        return self.search_similar(
            query=f"agent {agent_name} findings",
            n_results=limit,
            filter_metadata={"agent_name": agent_name}
        )
    
    def get_all_findings(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all stored findings."""
        results = self.collection.get(limit=limit)
        
        formatted_results = []
        if results['ids']:
            for i in range(len(results['ids'])):
                formatted_results.append({
                    "id": results['ids'][i],
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i]
                })
        
        return formatted_results
    
    def store_critique(self, 
                      target_agent: str,
                      critique_content: str,
                      critique_type: str = "feedback") -> str:
        """Store a critique from one agent to another."""
        metadata = {
            "target_agent": target_agent,
            "critique_type": critique_type
        }
        return self.store_document(
            content=critique_content,
            metadata=metadata,
            agent_name="Critic",
            document_type="critique"
        )
    
    def get_critiques_for_agent(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get all critiques for a specific agent."""
        # Use query with filter instead of get
        results = self.collection.get()
        
        # Filter results manually
        formatted_results = []
        if results['ids']:
            for i in range(len(results['ids'])):
                metadata = results['metadatas'][i]
                if (metadata.get("target_agent") == agent_name and 
                    metadata.get("document_type") == "critique"):
                    formatted_results.append({
                        "id": results['ids'][i],
                        "content": results['documents'][i],
                        "metadata": metadata
                    })
        
        return formatted_results

