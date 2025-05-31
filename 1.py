import os
import re
import json
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv

# Import from your approved role_agent.py
from role_agent import IntelligentRoleAgent, RoleAnalysisParser

load_dotenv()

class SmartTaskParser(BaseOutputParser):
    """Parser to extract tasks with dynamic allocation from AI response"""
    
    def parse(self, text: str) -> Dict[str, List[str]]:
        """Parse the AI response to extract tasks organized by roles"""
        
        try:
            # Try to parse as JSON first
            if '{' in text and '}' in text:
                start = text.find('{')
                end = text.rfind('}') + 1
                json_str = text[start:end]
                parsed_json = json.loads(json_str)
                
                # Extract role_tasks if it exists in the JSON structure
                if 'role_tasks' in parsed_json:
                    return parsed_json['role_tasks']
                elif 'tasks' in parsed_json:
                    return parsed_json['tasks']
                else:
                    # If JSON doesn't have expected structure, return the whole thing
                    return parsed_json
                    
        except json.JSONDecodeError:
            pass
        
        # Fallback to text parsing if JSON fails
        roles_tasks = {}
        lines = text.strip().split('\n')
        current_role = None
        current_tasks = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and separators
            if not line or line.startswith('=') or line.startswith('-') or line.startswith('*'):
                continue
            
            # Check if this is a role header (contains role name followed by colon)
            if ':' in line and not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                # Save previous role's tasks
                if current_role and current_tasks:
                    roles_tasks[current_role] = current_tasks.copy()
                
                # Extract new role name
                current_role = line.split(':')[0].strip()
                # Clean up role name formatting
                current_role = re.sub(r'^[🎨⚡🤖☁️💾🎯🔍📊🛡️📱🌐]\s*', '', current_role)
                current_role = re.sub(r'\*\*', '', current_role).strip()
                current_tasks = []
                continue
            
            # Check if this is a task (starts with number or bullet)
            task_match = re.match(r'^[\d+\.\-\*•▶️✨🔧⭐🚀]\s*(.+)', line)
            if task_match and current_role:
                task_text = task_match.group(1).strip()
                # Clean up any remaining emoji or formatting
                task_text = re.sub(r'^[▶️✨🔧⭐🚀]\s*', '', task_text)
                
                if len(task_text) > 15:  # Only include meaningful tasks
                    current_tasks.append(task_text)
        
        # Don't forget the last role
        if current_role and current_tasks:
            roles_tasks[current_role] = current_tasks
        
        return roles_tasks

class SmartTaskAgent:
    """Intelligent task generator that dynamically allocates tasks based on role complexity and project needs"""
    
    def __init__(self, api_key: str = None):
        """Initialize the smart task agent"""
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key is required! Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize LLM for task generation
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.7,  # Balanced creativity for diverse tasks
            max_tokens=4000   # Allow for detailed task descriptions
        )
        
        self.parser = SmartTaskParser()
        self.role_agent = IntelligentRoleAgent(api_key)
        self._setup_smart_task_prompt()
    
    def _setup_smart_task_prompt(self):
        """Create an intelligent prompt for dynamic task allocation"""
        
        template = """
You are an expert project architect and task allocation specialist. Your mission is to intelligently analyze each role's complexity and importance in the project, then generate the optimal number of tasks for each role.

PROJECT DESCRIPTION:
{project_description}

SELECTED ROLES:
{selected_roles}

INTELLIGENT TASK ALLOCATION FRAMEWORK:

STEP 1: ANALYZE ROLE COMPLEXITY & IMPORTANCE
For each role, consider:
- Amount of work required for this specific project
- Critical dependencies on other roles
- Unique value the role brings to the project

STEP 2: TASK QUALITY CRITERIA
- Each task should be specific, actionable, and technically detailed
- Include relevant technologies, frameworks, and tools
- Progressive complexity: foundation → features → integration → optimization
- Connect tasks logically within each role
- Ensure tasks integrate well across different roles

OUTPUT FORMAT:
Return your response as JSON in this exact format:
{{
  "role_tasks": {{
    "Role Name 1": [
      "Task 1 with specific technical details and technologies",
      "Task 2 with clear deliverables and implementation approach",
      "Task 3 with integration considerations and dependencies"
    ],
    "Role Name 2": [
      "Task 1 description...",
      "Task 2 description...",
      "Task 3 description...",
      "Task 4 description..."
    ]
  }}
}}

CRITICAL REQUIREMENTS:
- Allocate tasks based on ACTUAL PROJECT NEEDS, not fixed numbers
- Include cutting-edge technologies relevant to 2025
- Make tasks exciting and technically challenging
- Ensure logical progression and dependencies between tasks
- Consider the entire project lifecycle from setup to deployment

REMEMBER: The number of tasks should reflect the role's actual workload and importance in THIS SPECIFIC PROJECT. Think strategically about what each role actually needs to accomplish.
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_description", "selected_roles"],
            template=template
        )
    
    def generate_tasks_from_roles(self, project_description: str, selected_roles: List[str]) -> Dict[str, Any]:
        """
        Generate tasks dynamically based on role analysis
        
        Args:
            project_description (str): The project description
            selected_roles (List[str]): List of roles from role agent
            
        Returns:
            Dict containing role tasks
        """
        
        if not selected_roles:
            raise ValueError("No roles provided. Please provide roles from the role agent.")
        
        # Format roles for the prompt
        roles_text = "\n".join(f"- {role}" for role in selected_roles)
        
        try:
            # Generate tasks using AI
            chain = self.prompt | self.llm
            result = chain.invoke({
                "project_description": project_description,
                "selected_roles": roles_text
            })
            
            # Parse the response
            parsed_result = self.parser.parse(result.content)
            
            # If we got a dict with role_tasks, extract it properly
            if isinstance(parsed_result, dict):
                if 'role_tasks' in parsed_result:
                    tasks_dict = parsed_result['role_tasks']
                else:
                    # Assume the whole dict is the tasks
                    tasks_dict = parsed_result
            else:
                tasks_dict = parsed_result
            
            return {
                "role_tasks": tasks_dict
            }
            
        except Exception as e:
            print(f"Error generating tasks: {str(e)}")
            # Simple fallback
            fallback_tasks = {}
            for role in selected_roles:
                fallback_tasks[role] = [
                    f"Set up development environment for {role}",
                    f"Implement core functionality for {role}",
                    f"Test and optimize {role} components"
                ]
            
            return {
                "role_tasks": fallback_tasks
            }
    
    def generate_from_role_agent(self, project_description: str) -> Dict[str, Any]:
        """
        Complete workflow: Get roles from role agent, then generate tasks
        
        Args:
            project_description (str): The project description
            
        Returns:
            Dict containing roles and tasks
        """
        
        # Step 1: Get roles from role agent
        role_analysis = self.role_agent.get_role_recommendations(project_description)
        selected_roles = role_analysis.get('selected_roles', [])
        
        if not selected_roles:
            raise ValueError("Role agent did not return any roles")
        
        # Step 2: Generate tasks for those roles
        task_analysis = self.generate_tasks_from_roles(project_description, selected_roles)
        
        # Step 3: Combine results
        complete_analysis = {
            "selected_roles": selected_roles,
            "role_tasks": task_analysis["role_tasks"]
        }
        
        return complete_analysis

def main():
    """Demo the smart task agent"""
    
    print("SMART TASK AGENT")
    print("=" * 30)
    
    try:
        # Initialize smart task agent
        task_agent = SmartTaskAgent()
        print("Task Agent initialized successfully\n")
        
        # Test project
        test_project = "An enterprise blockchain-based supply chain management platform"
        
        print(f"Test Project: {test_project}\n")
        
        # Generate complete analysis
        analysis = task_agent.generate_from_role_agent(test_project)
        
        # Display results as JSON
        print(json.dumps(analysis, indent=2))
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your OpenAI API key in the .env file or environment variables")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()