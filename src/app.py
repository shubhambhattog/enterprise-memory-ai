from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from dotenv import load_dotenv

from .memory_service import MemoryService
from .chat_service import ChatService
from .config import get_config

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Enterprise Memory-Aware AI Assistant",
    description="AI Assistant with persistent memory and context awareness",
    version="1.0.0"
)

# Initialize services
config = get_config()
memory_service = MemoryService(config)
chat_service = ChatService(memory_service, config)


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    user_id: str
    conversation_id: str
    memory_added: bool


class MemoryResponse(BaseModel):
    memories: List[Dict[str, Any]]
    user_id: str
    total_count: int


# API Endpoints
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Enterprise Memory-Aware AI Assistant",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test database connections
        memory_health = memory_service.health_check()
        return {
            "status": "healthy",
            "services": {
                "memory": memory_health,
                "api": "running"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get context-aware response
    """
    try:
        response = await chat_service.process_message(
            message=request.message,
            user_id=request.user_id,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(**response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@app.get("/memory/{user_id}", response_model=MemoryResponse)
def get_user_memories(user_id: str, limit: int = 10):
    """
    Retrieve user's memories
    """
    try:
        memories = memory_service.get_user_memories(user_id, limit)
        
        return MemoryResponse(
            memories=memories,
            user_id=user_id,
            total_count=len(memories)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory retrieval failed: {str(e)}")


@app.delete("/memory/{user_id}")
def clear_user_memories(user_id: str):
    """
    Clear all memories for a user
    """
    try:
        success = memory_service.clear_user_memories(user_id)
        
        if success:
            return {"status": "success", "message": f"Memories cleared for user {user_id}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear memories")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory clearing failed: {str(e)}")


@app.get("/memory/{user_id}/search")
def search_memories(user_id: str, query: str, limit: int = 5):
    """
    Search user's memories by query
    """
    try:
        results = memory_service.search_memories(user_id, query, limit)
        
        return {
            "query": query,
            "user_id": user_id,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory search failed: {str(e)}")


@app.get("/analytics/{user_id}")
def get_user_analytics(user_id: str):
    """
    Get user interaction analytics
    """
    try:
        analytics = memory_service.get_user_analytics(user_id)
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")


def main():
    """Start the FastAPI application"""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
