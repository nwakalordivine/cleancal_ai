from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    response: str