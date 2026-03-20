from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    latency_ms: Optional[int] = None


class Turn(BaseModel):
    turn_id: int
    role: str
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    timestamp: str


class Annotation(BaseModel):
    label: str
    annotator_id: Optional[str] = None


class Feedback(BaseModel):
    user_rating: Optional[int] = None
    ops_review: Optional[Dict[str, Any]] = None
    annotations: Optional[List[Annotation]] = None


class ConversationSchema(BaseModel):
    conversation_id: str
    agent_version: str
    turns: List[Turn]
    feedback: Optional[Feedback]
    metadata: Optional[Dict[str, Any]]
