# CleanCal AI Agent API Documentation

---

**Base URL**: `http://127.0.0.1:8000`

---

## Ask the AI Agent

**URL**: `/ask-agent`

**Method**: `POST`

**Content-Type**: `application/json`

**Description**: This endpoint takes a user's natural language query, fetches relevant context from the 'reports' database table, and uses the Gemini AI to generate a natural language response.

**Body**: ```json { "query": "What is the scale of waste this period?" } ```

`query` (string, required): The natural language question you want to ask the agent.

**Response**: **200: Query successful** ```json { "response": "Well, according to CleanCal, the scale of waste has increased by 15% this period, with a high severity of plastic waste reported in the downtown area." } ```

**Errors**:

`500`: Error fetching data from database.

`500`: Error processing query with AI agent.

---