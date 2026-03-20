from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    latency_ms: Optional[int]


class Turn(BaseModel):
    turn_id: int
    role: str
    content: str
    tool_calls: Optional[List[ToolCall]]
    timestamp: str


class Feedback(BaseModel):
    user_rating: Optional[int]
    ops_review: Optional[Dict[str, Any]]
    annotations: Optional[List[Dict[str, Any]]]


class ConversationSchema(BaseModel):
    conversation_id: str
    agent_version: str
    turns: List[Turn]
    feedback: Optional[Feedback]
    metadata: Optional[Dict[str, Any]]
