import os
import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class SimpleRoleAgent:
    """Simple role selection agent that analyzes projects and selects optimal team roles"""
    
    # Simplified role taxonomy
    ROLE_TAXONOMY = {
        'Frontend Development': [
            'Web Frontend Developer',
            'Mobile Frontend Developer', 
            'Desktop Application Developer'
        ],
        'Backend Development': [
            'Backend Developer',
            'Database Specialist',
            'API Architect'
        ],
        'AI & Machine Learning': [
            'AI/ML Engineer',
            'Generative AI Engineer',
            'Data Scientist',
            'NLP Engineer',
            'Computer Vision Engineer'
        ],
        'Data Engineering': [
            'Data Engineer',
            'MLOps Engineer'
        ],
        'Cloud & Infrastructure': [
            'Cloud Engineer',
            'DevOps Engineer',
            'Security Engineer'
        ],
        'Design & User Experience': [
            'UI/UX Designer',
            'Product Designer',
            'Graphic Designer'
        ],
        'Quality Assurance': [
            'QA Engineer',
            'Performance Engineer'
        ],
        'Specialized Technologies': [
            'Blockchain Developer',
            'IoT Engineer',
            'Game Developer',
            'AR/VR Developer'
        ],
        'Management & Strategy': [
            'Technical Project Manager',
            'Product Manager',
            'Solution Architect'
        ]
    }
    
    def __init__(self):
        """Initialize the role agent with OpenAI API"""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        print(f"API Key loaded: {'Yes' if OPENAI_API_KEY else 'No'}")
        if OPENAI_API_KEY:
            print(f"API Key starts with: {OPENAI_API_KEY[:10]}...")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=OPENAI_API_KEY)
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Create simple prompt template for role selection"""
        
        # Convert role taxonomy to simple text format
        roles_text = ""
        for domain, roles in self.ROLE_TAXONOMY.items():
            roles_text += f"\n{domain}:\n"
            for role in roles:
                roles_text += f"  - {role}\n"
        
        template = """
You are a technical team composition expert. Analyze the project and select 3-6 most relevant roles.

PROJECT DESCRIPTION:
{project_description}

AVAILABLE ROLES:
{available_roles}

INSTRUCTIONS:
- Select only the most essential roles for this project
- Focus on roles that will have substantial ongoing work
- Return response as valid JSON format only

REQUIRED OUTPUT FORMAT:
{{"selected_roles": ["Role Name 1", "Role Name 2", "Role Name 3"]}}
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_description", "available_roles"],
            template=template
        )
        self.roles_text = roles_text
    
    def select_roles(self, project_description: str) -> Dict[str, List[str]]:
        """
        Select optimal roles for the project
        
        Args:
            project_description (str): Description of the project
            
        Returns:
            Dict with selected roles list
        """
        try:
            # Generate response from LLM
            chain = self.prompt | self.llm
            result = chain.invoke({
                "project_description": project_description,
                "available_roles": self.roles_text
            })
            # Handle JSON in markdown code blocks
            response_text = result.content.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                # Find the JSON content between code blocks
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
            return {"selected_roles": ["Frontend Developer", "Backend Developer"]}

def main():
    """Demo the simple role agent"""
    print("🎯 SIMPLE ROLE SELECTION AGENT")
    print("=" * 40)
    
    try:
        # Initialize agent
        agent = SimpleRoleAgent()
        print("✅ Agent initialized\n")
        
        # Test projects
        test_projects = [
            "An AI-powered assistant that creates LinkedIn blog posts from various content types",
            "A mobile fitness app with social features and AI workout recommendations",
            "An enterprise blockchain supply chain management platform"
        ]
        
        for i, project in enumerate(test_projects, 1):
            print(f"Project {i}: {project}")
            
            # Get role recommendations
            result = agent.select_roles(project)
            
            # Print JSON result
            print("Selected Roles:")
            print(json.dumps(result, indent=2))
            print("-" * 40)
        
    except ValueError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()