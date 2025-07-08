from openai import OpenAI
from typing import Dict, Any, List, Optional
import json
import uuid
from .memory_service import MemoryService


class ChatService:
    """Handles chat interactions with memory context"""
    
    def __init__(self, memory_service: MemoryService, config: Dict[str, Any]):
        self.memory_service = memory_service
        self.config = config
        self.client = OpenAI(api_key=config["openai"]["api_key"])
        self.model = config["openai"].get("model", "gpt-4")
    
    async def process_message(
        self, 
        message: str, 
        user_id: str, 
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a chat message with memory context"""
        
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        try:
            # Retrieve relevant memories
            relevant_memories = self.memory_service.search_memories(
                user_id=user_id,
                query=message,
                limit=5
            )
            
            # Build context from memories
            memory_context = self._build_memory_context(relevant_memories)
            
            # Generate AI response
            ai_response = self._generate_response(message, memory_context)
            
            # Store conversation in memory
            conversation = [
                {"role": "user", "content": message},
                {"role": "assistant", "content": ai_response}
            ]
            
            memory_ids = self.memory_service.add_conversation(
                messages=conversation,
                user_id=user_id
            )
            
            return {
                "response": ai_response,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "memory_added": len(memory_ids) > 0,
                "relevant_memories_count": len(relevant_memories)
            }
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            # Fallback response without memory
            fallback_response = self._generate_fallback_response(message)
            return {
                "response": fallback_response,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "memory_added": False,
                "error": str(e)
            }
    
    def _build_memory_context(self, memories: List[Dict[str, Any]]) -> str:
        """Build context string from relevant memories"""
        if not memories:
            return "No previous context available."
        
        context_parts = []
        for memory in memories:
            context_parts.append(f"Memory: {memory.get('memory', '')}")
        
        return "\n".join(context_parts)
    
    def _generate_response(self, message: str, memory_context: str) -> str:
        """Generate AI response using OpenAI with memory context"""
        system_prompt = f"""
        You are an intelligent, memory-aware AI assistant. You have access to the user's previous conversations and important facts about them.

        Use the following context from the user's memory to provide personalized, contextual responses:

        {memory_context}

        Instructions:
        - Be conversational and helpful
        - Reference relevant memories when appropriate
        - Maintain consistency with previous interactions
        - If you don't have relevant context, respond naturally
        - Don't explicitly mention that you're using "memories" unless asked
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return self._generate_fallback_response(message)
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate a fallback response without memory context"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use cheaper model for fallback
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful AI assistant. Respond to the user's message naturally."
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. (Error: {str(e)})"
    
    def get_conversation_summary(self, user_id: str, conversation_id: str) -> str:
        """Get a summary of a conversation"""
        try:
            # Get memories related to this conversation
            memories = self.memory_service.get_user_memories(user_id, limit=50)
            
            conversation_memories = [
                m for m in memories 
                if m.get("metadata", {}).get("conversation_id") == conversation_id
            ]
            
            if not conversation_memories:
                return "No conversation found."
            
            # Build conversation text
            conversation_text = "\n".join([
                m.get("memory", "") for m in conversation_memories
            ])
            
            # Generate summary
            summary_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize the following conversation in 2-3 sentences:"
                    },
                    {"role": "user", "content": conversation_text}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            return summary_response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
