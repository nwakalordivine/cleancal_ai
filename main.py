from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import agent
from database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CleanCal AI Agent",
    description="An API for querying waste reports with a Gemini AI agent."
)

@app.post("/ask-agent", response_model=schemas.AgentResponse)
def ask_agent(
    request: schemas.QueryRequest,
    db: Session = Depends(get_db)
):
    """
    This is the single endpoint for your AI agent.
    
    It takes a user's query, fetches relevant data from the 'reports'
    table, and then uses Gemini to generate a natural language response.
    """
    
    print(f"Fetching context for query: {request.query}")
    try:
        context = agent.get_report_context(db, request.query)
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from database.")

    print("Context fetched, calling Gemini...")
    try:
        ai_response = agent.get_gemini_response(context, request.query)
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise HTTPException(status_code=500, detail="Error processing query with AI agent.")
    return schemas.AgentResponse(response=ai_response)

@app.get("/")
def read_root():
    return {"message": "CleanCal AI Agent is running. POST to /ask-agent"}