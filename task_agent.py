import os
import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from role_agent import SimpleRoleAgent

load_dotenv()

class SimpleTaskAgent:
    """Simple task generator that creates tasks based on selected roles"""
    
    def __init__(self):
        """Initialize the task agent with OpenAI API"""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=OPENAI_API_KEY)
        self.role_agent = SimpleRoleAgent()
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Create simple prompt template for task generation"""
        
        template = """
You are a project task allocation expert. Generate 3-5 specific tasks for each role based on the project.

PROJECT DESCRIPTION:
{project_description}

SELECTED ROLES:
{selected_roles}

INSTRUCTIONS:
- Create 3-5 specific, actionable tasks for each role
- Make tasks relevant to the project requirements
- Include technical details and tools where appropriate
- Return response as valid JSON format only

REQUIRED OUTPUT FORMAT:
{{
  "role_tasks": {{
    "Role Name 1": [
      "Task 1 description",
      "Task 2 description", 
      "Task 3 description"
    ],
    "Role Name 2": [
      "Task 1 description",
      "Task 2 description",
      "Task 3 description",
      "Task 4 description"
    ]
  }}
}}
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_description", "selected_roles"],
            template=template
        )
    
    def generate_tasks(self, project_description: str, selected_roles: List[str]) -> Dict[str, any]:
        """
        Generate tasks for the given roles
        
        Args:
            project_description (str): Description of the project
            selected_roles (List[str]): List of selected roles
            
        Returns:
            Dict with role tasks
        """
        # Format roles for prompt
        roles_text = "\n".join(f"- {role}" for role in selected_roles)
        
        try:
            # Generate response from LLM
            chain = self.prompt | self.llm
            result = chain.invoke({
                "project_description": project_description,
                "selected_roles": roles_text
            })
            
            # Handle JSON in markdown code blocks
            response_text = result.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                json_lines = []
                in_json = False
                for line in lines:
                    if line.startswith('```'):
                        in_json = not in_json
                        continue
                    if in_json:
                        json_lines.append(line)
                response_text = '\n'.join(json_lines).strip()
            
            return json.loads(response_text)
                
        except Exception as e:
            print(f"Error: {e}")
            # Fallback response
            fallback_tasks = {}
            for role in selected_roles:
                fallback_tasks[role] = [
                    f"Set up development environment for {role}",
                    f"Implement core functionality",
                    f"Test and optimize components"
                ]
            return {"role_tasks": fallback_tasks}
    
    def analyze_project(self, project_description: str) -> Dict[str, any]:
        """
        Complete workflow: Get roles and generate tasks
        
        Args:
            project_description (str): Description of the project
            
        Returns:
            Dict with selected roles and their tasks
        """
        # Step 1: Get roles from role agent
        role_result = self.role_agent.select_roles(project_description)
        selected_roles = role_result.get('selected_roles', [])
        
        # Step 2: Generate tasks for those roles
        task_result = self.generate_tasks(project_description, selected_roles)
        
        # Step 3: Combine results
        return {
            "selected_roles": selected_roles,
            "role_tasks": task_result.get("role_tasks", {})
        }

def main():
    """Demo the simple task agent"""
    print("🎯 SIMPLE TASK AGENT")
    print("=" * 30)
    
    try:
        # Initialize agent
        agent = SimpleTaskAgent()
        print("✅ Agent initialized\n")
        
        # Test projects
        test_projects = [
            "An AI-powered assistant that creates LinkedIn blog posts from various content types",
            "A mobile fitness app with social features and AI workout recommendations"
        ]
        
        for i, project in enumerate(test_projects, 1):
            print(f"Project {i}: {project}")
            
            # Get complete analysis
            result = agent.analyze_project(project)
            
            # Print JSON result
            print("Analysis Result:")
            print(json.dumps(result, indent=2))
            print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()