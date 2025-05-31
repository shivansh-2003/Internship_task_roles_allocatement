from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Import the task agent
from task_agent import SmartTaskAgent

load_dotenv()

app = FastAPI(
    title="Smart Task Agent API",
    description="API for generating roles and tasks for projects using AI",
    version="1.0.0"
)

# Request model
class ProjectRequest(BaseModel):
    project_description: str

# Response model
class TaskResponse(BaseModel):
    selected_roles: list
    role_tasks: Dict[str, list]

# Initialize the task agent
try:
    task_agent = SmartTaskAgent()
except Exception as e:
    print(f"Error initializing task agent: {e}")
    task_agent = None

@app.post("/generate-tasks", response_model=TaskResponse)
async def generate_tasks(request: ProjectRequest):
    """
    Generate roles and tasks for a project description
    
    Args:
        request: ProjectRequest containing project_description
        
    Returns:
        TaskResponse with selected_roles and role_tasks
    """
    
    if not task_agent:
        raise HTTPException(
            status_code=500, 
            detail="Task agent not initialized. Please check OpenAI API key configuration."
        )
    
    if not request.project_description.strip():
        raise HTTPException(
            status_code=400, 
            detail="Project description cannot be empty"
        )
    
    try:
        # Generate roles and tasks
        result = task_agent.generate_from_role_agent(request.project_description)
        
        return TaskResponse(
            selected_roles=result.get("selected_roles", []),
            role_tasks=result.get("role_tasks", {})
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating tasks: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 