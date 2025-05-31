from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import json
from task_agent import CreativeProjectBreakdownAgent
from output_formatter import OutputFormatter

# Initialize FastAPI app
app = FastAPI(
    title="Creative Project Breakdown API",
    description="Transform your project ideas into actionable task breakdowns for different roles",
    version="1.0.0"
)

# Initialize components
try:
    task_agent = CreativeProjectBreakdownAgent()
    output_formatter = OutputFormatter()
except Exception as e:
    print(f"Error initializing components: {str(e)}")
    task_agent = None
    output_formatter = None

# Pydantic models for request/response
class ProjectRequest(BaseModel):
    project_idea: str = Field(..., description="Description of the project idea", min_length=10, max_length=1000)
    format_type: Optional[str] = Field(default="json", description="Output format: 'json' or 'formatted'")

class TaskBreakdownResponse(BaseModel):
    project_name: str
    roles_and_responsibilities: Dict[str, List[str]]
    summary: Dict[str, int]
    status: str = "success"

class FormattedResponse(BaseModel):
    formatted_output: str
    status: str = "success"

class ErrorResponse(BaseModel):
    error: str
    status: str = "error"

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Creative Project Breakdown API",
        "description": "Send your project idea to /breakdown endpoint to get actionable task breakdowns",
        "endpoints": {
            "POST /breakdown": "Generate project task breakdown",
            "GET /health": "Check API health status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if task_agent is None or output_formatter is None:
        raise HTTPException(status_code=503, detail="Service components not properly initialized")
    
    return {
        "status": "healthy",
        "components": {
            "task_agent": "initialized" if task_agent else "failed",
            "output_formatter": "initialized" if output_formatter else "failed"
        }
    }

@app.post("/breakdown", response_model=TaskBreakdownResponse)
async def create_project_breakdown(request: ProjectRequest):
    """
    Generate a project breakdown with tasks for different roles
    
    This endpoint takes a project description and returns:
    - Role-based task breakdowns
    - Clean JSON format
    - Project summary statistics
    """
    
    if task_agent is None or output_formatter is None:
        raise HTTPException(
            status_code=503, 
            detail="Service not available - components not properly initialized"
        )
    
    try:
        # Step 1: Generate task breakdown using the agent
        tasks_dict = task_agent.breakdown_project(request.project_idea)
        
        if not tasks_dict:
            raise HTTPException(
                status_code=422,
                detail="Could not generate meaningful tasks for this project idea. Please provide more details."
            )
        
        # Step 2: Format the output
        formatted_output = task_agent.format_output(tasks_dict, request.project_idea)
        
        # Step 3: Parse the formatted output to clean JSON
        parsed_data = output_formatter.parse_formatted_output(formatted_output)
        
        return TaskBreakdownResponse(
            project_name=parsed_data["project_name"],
            roles_and_responsibilities=parsed_data["roles_and_responsibilities"],
            summary=parsed_data["summary"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/breakdown/formatted", response_model=FormattedResponse)
async def create_formatted_breakdown(request: ProjectRequest):
    """
    Generate a project breakdown with formatted text output
    
    This endpoint returns the same breakdown but in formatted text format
    instead of clean JSON structure.
    """
    
    if task_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="Service not available - task agent not properly initialized"
        )
    
    try:
        # Generate task breakdown using the agent
        tasks_dict = task_agent.breakdown_project(request.project_idea)
        
        if not tasks_dict:
            raise HTTPException(
                status_code=422,
                detail="Could not generate meaningful tasks for this project idea. Please provide more details."
            )
        
        # Format the output
        formatted_output = task_agent.format_output(tasks_dict, request.project_idea)
        
        return FormattedResponse(
            formatted_output=formatted_output
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/breakdown/json", response_model=str)
async def create_json_breakdown(request: ProjectRequest):
    """
    Generate a project breakdown and return as JSON string
    
    This endpoint returns the breakdown as a JSON string for easy integration
    with other systems.
    """
    
    if task_agent is None or output_formatter is None:
        raise HTTPException(
            status_code=503, 
            detail="Service not available - components not properly initialized"
        )
    
    try:
        # Generate task breakdown using the agent
        tasks_dict = task_agent.breakdown_project(request.project_idea)
        
        if not tasks_dict:
            raise HTTPException(
                status_code=422,
                detail="Could not generate meaningful tasks for this project idea. Please provide more details."
            )
        
        # Format the output
        formatted_output = task_agent.format_output(tasks_dict, request.project_idea)
        
        # Convert to JSON string
        json_output = output_formatter.format_to_json(formatted_output, pretty_print=True)
        
        return json_output
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status": "error",
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": "An unexpected error occurred",
        "status": "error",
        "status_code": 500
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 