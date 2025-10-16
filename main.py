from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="IntelliChat AI Assistant",
    description="A smart AI-powered chat assistant API built with FastAPI",
    version="1.0.0"
)

# Data models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    timestamp: str

# Simple in-memory conversation storage
conversations = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "IntelliChat AI Assistant API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": ["/chat", "/health", "/conversations"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "IntelliChat AI"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint that processes user messages"""
    import datetime
    
    # Simple response generation (in production, integrate with AI model)
    responses = [
        "That's an interesting question! Let me help you with that.",
        "I understand. Here's what I think about that topic.",
        "Great question! Based on the information available, I'd say...",
        "Let me process that for you. Here's my analysis.",
        "Thank you for asking! Here's a thoughtful response."
    ]
    
    # Simple hash to get consistent response per message
    response_text = responses[len(request.message) % len(responses)]
    
    return ChatResponse(
        response=response_text,
        timestamp=datetime.datetime.now().isoformat()
    )

@app.get("/conversations")
async def get_conversations():
    """Retrieve all conversation IDs"""
    return {"conversations": list(conversations.keys()), "count": len(conversations)}

@app.post("/conversations/{conversation_id}")
async def save_conversation(conversation_id: str, messages: List[Message]):
    """Save a conversation to memory"""
    conversations[conversation_id] = [msg.dict() for msg in messages]
    return {"message": "Conversation saved", "id": conversation_id}

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Retrieve a specific conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"id": conversation_id, "messages": conversations[conversation_id]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
