import os
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import json
import re
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class SmartProjectTaskParser(BaseOutputParser):
    """Advanced parser to extract role-based tasks with intelligent filtering"""
    
    def parse(self, text: str) -> Dict[str, List[str]]:
        roles_tasks = {}
        
        # Split by role sections - looking for patterns like "Frontend Developer:" or "Backend Developer:"
        sections = re.split(r'\n(?=[A-Z][^:]*:)', text.strip())
        
        for section in sections:
            if ':' in section:
                lines = section.strip().split('\n')
                
                # Extract role name (remove colon)
                role_line = lines[0]
                role = role_line.replace(':', '').strip()
                
                tasks = []
                for line in lines[1:]:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('---'):
                        # Clean up task formatting
                        task = re.sub(r'^[-•*\d+\.\)]\s*', '', line).strip()
                        
                        if task and len(task) > 10:  # Filter out very short/empty tasks
                            tasks.append(task)
                
                if tasks and len(tasks) >= 2:  # Only include roles with meaningful tasks
                    roles_tasks[role] = tasks
        
        return roles_tasks

class CreativeProjectTaskAgent:
    """Enhanced AI Agent focused on task generation for pre-selected roles"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required!")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.8, max_tokens=2000)
        self.parser = SmartProjectTaskParser()
        self._setup_task_generation_prompt()
    
    def _setup_task_generation_prompt(self):
        """Setup an enhanced, creative prompt template for task generation"""
        
        template = """
PROJECT TASK STRATEGIST

You are an elite project architect specializing in creating actionable task breakdowns.

PROJECT: {project_description}
ASSIGNED ROLES: {selected_roles}

TASK GENERATION GUIDELINES:
1. Create 4-5 specific, actionable tasks for each assigned role
2. Include concrete technologies and frameworks (React 18, TensorFlow, Apache Kafka, etc.)
3. Focus on practical implementation with technical depth
4. Consider integration points between different roles
5. Balance foundational work with innovative features
6. Make tasks exciting challenges with clear business value
7. Each task should be 15-25 words for optimal readability
8. Progressive complexity: foundation -> features -> implementation -> integration -> optimization

OUTPUT FORMAT (use EXACTLY this format):

Frontend Developer:
1. [Specific actionable task with technical details - mention specific frameworks/libraries]
2. [Another concrete task that sounds exciting and innovative]
3. [Implementation-focused task with technical depth]
4. [Integration or collaboration task]
5. [Advanced/optimization task for performance/scalability]

Backend Developer:
1. [Architecture and API design task with specific technologies]
2. [Authentication/security implementation task]
3. [Database design and optimization task]
4. [API documentation and integration task]
5. [Performance optimization and scalability task]

AI/ML Engineer:
1. [ML model development task with specific algorithms]
2. [AI feature implementation with practical applications]
3. [Data preprocessing and pipeline task]
4. [Model integration with backend services]
5. [MLOps and model monitoring task]

UI/UX Designer:
1. [User research and persona development]
2. [Information architecture and user journey design]
3. [High-fidelity mockups and prototyping]
4. [Developer collaboration for implementation]
5. [Usability testing and optimization]

Cloud & DevOps Engineer:
1. [Cloud infrastructure design with specific platforms]
2. [CI/CD pipeline setup with automation tools]
3. [Containerization and orchestration task]
4. [Monitoring and logging implementation]
5. [Cost optimization and scaling strategies]

Data Engineer:
1. [ETL pipeline design with specific tools]
2. [Real-time data streaming implementation]
3. [Data lake/warehouse architecture]
4. [Data quality and validation frameworks]
5. [Data governance and analytics platform]

IMPORTANT: Only create tasks for the roles listed in ASSIGNED ROLES. Generate exciting, technically detailed tasks that teams will be motivated to work on!
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_description", "selected_roles"],
            template=template
        )
    
    def generate_tasks_for_roles(self, project_description: str, selected_roles: List[str]) -> Dict[str, Any]:
        """Generate tasks for pre-selected roles and return JSON structure"""
        
        # Create role string
        selected_roles_str = ", ".join(selected_roles)
        
        try:
            # Generate the breakdown using new syntax
            chain = self.prompt | self.llm
            result = chain.invoke({
                "project_description": project_description,
                "selected_roles": selected_roles_str
            })
            
            # Parse and return
            parsed_result = self.parser.parse(result.content)
            
            # Convert to the JSON structure expected by output_formatter
            json_structure = {
                "project_name": project_description,
                "roles_and_responsibilities": parsed_result,
                "summary": {
                    "total_roles": len(parsed_result),
                    "total_tasks": sum(len(tasks) for tasks in parsed_result.values())
                }
            }
            
            return json_structure
            
        except Exception as e:
            print(f"Error processing task generation: {str(e)}")
            return {
                "project_name": project_description,
                "roles_and_responsibilities": {},
                "summary": {
                    "total_roles": 0,
                    "total_tasks": 0
                }
            }
    
    def generate_tasks_json(self, project_description: str, selected_roles: List[str]) -> str:
        """Generate tasks and return as JSON string"""
        json_data = self.generate_tasks_for_roles(project_description, selected_roles)
        return json.dumps(json_data, indent=2, ensure_ascii=False)

# Integrated Project Breakdown System
class IntegratedProjectBreakdownSystem:
    """Complete system that combines role selection and task generation"""
    
    def __init__(self):
        try:
            from role_agent import SmartRoleAgent
            self.role_agent = SmartRoleAgent()
        except ImportError:
            print("Warning: role_agent not found, will use fallback role selection")
            self.role_agent = None
        
        self.task_agent = CreativeProjectTaskAgent()
    
    def process_project(self, project_description: str) -> Dict[str, Any]:
        """Complete project processing: role selection + task generation"""
        
        # Step 1: Select roles
        if self.role_agent:
            selected_roles = self.role_agent.select_roles(project_description)
            print(f"Selected roles: {', '.join(selected_roles)}")
        else:
            # Fallback role selection
            selected_roles = ['Frontend Developer', 'Backend Developer', 'AI/ML Engineer']
            print(f"Using fallback roles: {', '.join(selected_roles)}")
        
        # Step 2: Generate tasks
        json_result = self.task_agent.generate_tasks_for_roles(project_description, selected_roles)
        
        return json_result
    
    def process_project_json(self, project_description: str) -> str:
        """Process project and return JSON string"""
        result = self.process_project(project_description)
        return json.dumps(result, indent=2, ensure_ascii=False)

def main():
    """Interactive main function with enhanced UX"""
    
    print("""
==================================================================
               INTEGRATED PROJECT BREAKDOWN SYSTEM              
                                                                  
        Transform your ideas into actionable roadmaps!           
==================================================================
    """)
    
    try:
        system = IntegratedProjectBreakdownSystem()
        print("System initialized successfully")
    except ValueError as e:
        print(str(e))
        return
    
    while True:
        print("\n" + "=" * 70)
        project_idea = input("Describe your project idea (or 'quit' to exit): ").strip()
        
        if project_idea.lower() in ['quit', 'exit', 'q']:
            print("Thanks for using the Integrated Project Breakdown System! Build something amazing!")
            break
        
        if not project_idea:
            print("Please enter a valid project idea!")
            continue
        
        print("\nStep 1: Selecting optimal roles...")
        print("Step 2: Generating creative task breakdown...")
        
        json_data = system.process_project(project_idea)
        
        if json_data and json_data["roles_and_responsibilities"]:
            print("\n" + "="*70)
            print("PROJECT BREAKDOWN (JSON FORMAT)")
            print("="*70)
            print(json.dumps(json_data, indent=2, ensure_ascii=False))
            
            save_choice = input("\nSave this breakdown? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                # Save to file
                safe_name = re.sub(r'[^\w\s-]', '', project_idea[:50]).strip()
                safe_name = re.sub(r'[-\s]+', '_', safe_name)
                filename = f"{safe_name}_breakdown.json"
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=2, ensure_ascii=False)
                    print(f"Project breakdown saved to {filename}")
                except Exception as e:
                    print(f"Error saving file: {str(e)}")
        else:
            print("Failed to process the project idea. Please try again with more details.")

if __name__ == "__main__":
    main()