# Creative Project Breakdown API

Transform your project ideas into actionable task breakdowns for different roles using AI.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file in the TASK2 directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Run the API:**
```bash
python api.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/`
Root endpoint with API information

### GET `/health`
Health check endpoint to verify all components are working

### POST `/breakdown`
Main endpoint to generate project breakdown

**Request Body:**
```json
{
  "project_idea": "Build an e-commerce platform with AI-powered recommendations"
}
```

**Response:**
```json
{
  "project_name": "Build an e-commerce platform with AI-powered recommendations",
  "roles_and_responsibilities": {
    "Frontend Developer": [
      "Design and implement responsive React-based product catalog with advanced filtering capabilities",
      "Create dynamic shopping cart system with real-time price calculations and inventory updates",
      "Build interactive user dashboard for order tracking and recommendation preferences management",
      "Integrate AI recommendation widget with seamless user experience and performance optimization"
    ],
    "Backend Developer": [
      "Architect scalable Node.js API with microservices for user management and product catalog",
      "Implement secure JWT-based authentication system with role-based access control mechanisms",
      "Design PostgreSQL database schema optimized for e-commerce transactions and user behavior tracking",
      "Create comprehensive API documentation using Swagger with integration testing frameworks",
      "Optimize database queries and implement Redis caching for high-performance product recommendations"
    ]
  },
  "summary": {
    "total_roles": 2,
    "total_tasks": 9
  },
  "status": "success"
}
```

### POST `/breakdown/formatted`
Returns formatted text output instead of JSON structure

### POST `/breakdown/json`
Returns the breakdown as a JSON string

## Usage Examples

### Using curl:
```bash
curl -X POST "http://localhost:8000/breakdown" \
  -H "Content-Type: application/json" \
  -d '{"project_idea": "Build a social media app with real-time messaging"}'
```

### Using Python requests:
```python
import requests

response = requests.post("http://localhost:8000/breakdown", 
                        json={"project_idea": "Create a task management app with AI scheduling"})
print(response.json())
```

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Features

- **Intelligent Role Selection**: Automatically determines relevant roles based on project requirements
- **AI-Powered Task Generation**: Creates specific, actionable tasks with technical details
- **Multiple Output Formats**: JSON, formatted text, or JSON string
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Health Monitoring**: Built-in health check endpoint
- **Interactive Documentation**: Auto-generated API documentation

## Project Structure

```
TASK2/
├── task_agent.py          # Core AI agent for task breakdown
├── output_formatter.py    # Formats output into clean JSON
├── api.py                # FastAPI application
├── requirements.txt      # Python dependencies
└── README.md            # This file
``` 