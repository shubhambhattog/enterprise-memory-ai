"""
Memory management service using Mem0, Neo4j, and Qdrant
"""

from mem0 import Memory
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime


class MemoryService:
    """Handles memory storage, retrieval, and management"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mem_client = Memory.from_config(config["memory"])
        
    def add_memory(self, content: str, user_id: str, metadata: Optional[Dict] = None) -> str:
        """Add a new memory for a user"""
        try:
            memory_data = {
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            result = self.mem_client.add(content, user_id=user_id, metadata=memory_data)
            return result.get("id", str(uuid.uuid4()))
            
        except Exception as e:
            print(f"Error adding memory: {str(e)}")
            raise
    
    def search_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant memories"""
        try:
            results = self.mem_client.search(query=query, user_id=user_id, limit=limit)
            
            memories = []
            for result in results.get("results", []):
                memories.append({
                    "id": result.get("id"),
                    "memory": result.get("memory"),
                    "score": result.get("score", 0),
                    "metadata": result.get("metadata", {})
                })
            
            return memories
            
        except Exception as e:
            print(f"Error searching memories: {str(e)}")
            return []
    
    def get_user_memories(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get all memories for a user"""
        try:
            result = self.mem_client.get_all(user_id=user_id)
            
            memories = []
            for memory in result.get("results", [])[:limit]:
                memories.append({
                    "id": memory.get("id"),
                    "memory": memory.get("memory"),
                    "created_at": memory.get("created_at"),
                    "metadata": memory.get("metadata", {})
                })
            
            return memories
            
        except Exception as e:
            print(f"Error getting user memories: {str(e)}")
            return []
    
    def clear_user_memories(self, user_id: str) -> bool:
        """Clear all memories for a user"""
        try:
            self.mem_client.delete_all(user_id=user_id)
            return True
            
        except Exception as e:
            print(f"Error clearing memories: {str(e)}")
            return False
    
    def add_conversation(self, messages: List[Dict[str, str]], user_id: str) -> List[str]:
        """Add a conversation (multiple messages) to memory"""
        try:
            memory_ids = []
            
            for message in messages:
                content = f"{message['role']}: {message['content']}"
                memory_id = self.add_memory(content, user_id, {
                    "type": "conversation",
                    "role": message['role']
                })
                memory_ids.append(memory_id)
            
            return memory_ids
            
        except Exception as e:
            print(f"Error adding conversation: {str(e)}")
            raise
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics for a user's memory usage"""
        try:
            memories = self.get_user_memories(user_id, limit=1000)
            
            total_memories = len(memories)
            conversation_memories = len([m for m in memories 
                                       if m.get("metadata", {}).get("type") == "conversation"])
            
            # Calculate memory distribution by type
            memory_types = {}
            for memory in memories:
                mem_type = memory.get("metadata", {}).get("type", "general")
                memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
            
            return {
                "user_id": user_id,
                "total_memories": total_memories,
                "conversation_memories": conversation_memories,
                "memory_distribution": memory_types,
                "last_activity": memories[0].get("created_at") if memories else None
            }
            
        except Exception as e:
            print(f"Error getting analytics: {str(e)}")
            return {"error": str(e)}
    
    def health_check(self) -> str:
        """Check if memory service is healthy"""
        try:
            # Try a simple operation
            test_result = self.mem_client.search("test", user_id="health_check", limit=1)
            return "healthy"
            
        except Exception as e:
            return f"unhealthy: {str(e)}"
