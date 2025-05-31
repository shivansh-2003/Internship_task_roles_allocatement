import os
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
import json
import re
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ProjectTaskParser(BaseOutputParser):
    """Custom parser to extract role-based tasks from LLM response"""
    
    def parse(self, text: str) -> Dict[str, List[str]]:
        # Parse the structured response into a dictionary
        roles_tasks = {}
        
        # Split by role sections
        sections = re.split(r'\n(?=[A-Z][^:]*:)', text.strip())
        
        for section in sections:
            if ':' in section:
                lines = section.strip().split('\n')
                role = lines[0].replace(':', '').strip()
                tasks = []
                
                for line in lines[1:]:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Remove bullet points and numbers
                        task = re.sub(r'^[-•*\d+\.\)]\s*', '', line).strip()
                        if task:
                            tasks.append(task)
                
                if tasks:
                    roles_tasks[role] = tasks
        
        return roles_tasks

class AIProjectBreakdownAgent:
    """AI Agent that breaks down project ideas into role-specific tasks"""
    
    def __init__(self, openai_api_key: str):
        """
        Initialize the agent with OpenAI API key
        
        Args:
            openai_api_key (str): Your OpenAI API key
        """
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.llm = ChatOpenAI(temperature=0.7, max_tokens=2000)
        self.parser = ProjectTaskParser()
        self._setup_prompt_template()
    
    def _setup_prompt_template(self):
        """Setup the prompt template for task breakdown"""
        
        template = """
You are an expert project manager and technical architect. Break down the following project idea into specific, actionable tasks for different professional roles.

Project Idea: {project_idea}

Please provide a detailed breakdown with tasks for each relevant role. Format your response exactly as shown below:

Frontend Developer:
- Task 1 description
- Task 2 description
- Task 3 description

Backend Developer:
- Task 1 description
- Task 2 description
- Task 3 description

AI Engineer:
- Task 1 description
- Task 2 description
- Task 3 description

Cloud & DevOps Engineer:
- Task 1 description
- Task 2 description
- Task 3 description

Data Engineer:
- Task 1 description
- Task 2 description

UI/UX Designer:
- Task 1 description
- Task 2 description

QA Engineer:
- Task 1 description
- Task 2 description



Guidelines:
1. Include only roles that are relevant to the project
2. Each task should be specific and actionable
3. Tasks should be technically accurate for each role
4. Consider the full project lifecycle from planning to deployment
5. Include integration points between different roles
6. Focus on practical implementation steps
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_idea"],
            template=template
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            output_parser=self.parser
        )
    
    def breakdown_project(self, project_idea: str) -> Dict[str, List[str]]:
        """
        Break down a project idea into role-specific tasks
        
        Args:
            project_idea (str): The project description to break down
            
        Returns:
            Dict[str, List[str]]: Dictionary with roles as keys and task lists as values
        """
        try:
            result = self.chain.run(project_idea=project_idea)
            return result
        except Exception as e:
            print(f"Error processing project breakdown: {str(e)}")
            return {}
    
    def format_output(self, tasks_dict: Dict[str, List[str]]) -> str:
        """
        Format the tasks dictionary into a readable string
        
        Args:
            tasks_dict (Dict[str, List[str]]): Dictionary of role-based tasks
            
        Returns:
            str: Formatted string representation
        """
        output = "🚀 PROJECT BREAKDOWN\n" + "="*50 + "\n\n"
        
        for role, tasks in tasks_dict.items():
            output += f"👤 {role.upper()}:\n"
            output += "-" * (len(role) + 5) + "\n"
            
            for i, task in enumerate(tasks, 1):
                output += f"{i}. {task}\n"
            output += "\n"
        
        return output
    
    def save_breakdown(self, tasks_dict: Dict[str, List[str]], filename: str = "project_breakdown.json"):
        """
        Save the project breakdown to a JSON file
        
        Args:
            tasks_dict (Dict[str, List[str]]): Dictionary of role-based tasks
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tasks_dict, f, indent=2, ensure_ascii=False)
            print(f"✅ Project breakdown saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")

def main():
    """
    Main function to demonstrate the AI Project Breakdown Agent
    """
    print("🤖 AI Project Breakdown Agent")
    print("="*40)
    
    # Get OpenAI API key
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ OpenAI API key is required!")
        return
    
    # Initialize the agent
    agent = AIProjectBreakdownAgent(api_key)
    
    while True:
        print("\n" + "="*50)
        project_idea = input("Enter your project idea (or 'quit' to exit): ").strip()
        
        if project_idea.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not project_idea:
            print("❌ Please enter a valid project idea!")
            continue
        
        print("\n🔄 Processing your project idea...")
        
        # Break down the project
        tasks = agent.breakdown_project(project_idea)
        
        if tasks:
            # Display the results
            formatted_output = agent.format_output(tasks)
            print("\n" + formatted_output)
            
            # Ask if user wants to save
            save_choice = input("💾 Save this breakdown to a file? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                filename = input("Enter filename (default: project_breakdown.json): ").strip()
                if not filename:
                    filename = "project_breakdown.json"
                agent.save_breakdown(tasks, filename)
        else:
            print("❌ Failed to process the project idea. Please try again.")

# Example usage
if __name__ == "__main__":
    # You can also use it programmatically like this:
    
    # Initialize with your API key
    # agent = AIProjectBreakdownAgent("your-openai-api-key-here")
    
    # Example project breakdown
    # project = "Build a full stack AI marketing agent"
    # tasks = agent.breakdown_project(project)
    # print(agent.format_output(tasks))
    
    # Run the interactive version
    main()