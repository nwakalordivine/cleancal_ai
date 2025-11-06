import os
import google.generativeai as genai
from sqlalchemy.orm import Session
import models
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def get_report_context(db: Session, user_query: str) -> str:
    """
    Fetches the 50 most recent reports from the database and serializes
    them into a string format for the AI.
    """

    recent_reports = db.query(models.Report).order_by(models.Report.created_at.desc()).limit(50).all()
    
    context_list = []
    for report in recent_reports:
        context_list.append({
            "title": report.title,
            "description": report.description,
            "status": report.status,
            "severity": report.severity,
            "category": report.category,
            "type": report.type,
            "created_at": report.created_at.isoformat(),
            "is_resolved": report.is_resolved
        })
    
    # Convert the list of reports to a JSON string
    return json.dumps(context_list, indent=2)


def get_gemini_response(context: str, query: str) -> str:
    """
    Sends the database context and user query to Gemini for a final answer.
    """
    
    # This is the most important part: the prompt.
    # It instructs the AI on its name, its data source, and its behavior.
    prompt = f"""
    You are an AI assistant for an application named "CleanCal".
    Your name is 'CleanCal'.

    You must answer the user's question based *only* on the following context,
    which is a JSON list of recent waste reports from the database.
    Do not make up information. If the answer isn't in the context,
    say so.

    When you answer, you MUST start your response with: "Well, according to CleanCal, "
    
    CONTEXT:
    {context}
    
    USER QUESTION:
    {query}
    
    CleanCal's Answer:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I'm having trouble analyzing the reports right now."