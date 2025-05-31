import os
from typing import Dict, List, Set
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import json
import re

class SmartProjectTaskParser(BaseOutputParser):
    """Advanced parser to extract role-based tasks with intelligent filtering"""
    
    def parse(self, text: str) -> Dict[str, List[str]]:
        roles_tasks = {}
        
        # Split by role sections - looking for patterns like "🎨 Frontend Developer:" or "⚡ Backend Developer:"
        sections = re.split(r'\n(?=(?:🎨|⚡|🤖|☁️|💾|🎯|🔍|📊|🛡️|📱|🌐)\s*[A-Z][^:]*:)', text.strip())
        
        for section in sections:
            if ':' in section and any(emoji in section for emoji in ['🎨', '⚡', '🤖', '☁️', '💾', '🎯', '🔍', '📊', '🛡️', '📱', '🌐']):
                lines = section.strip().split('\n')
                
                # Extract role name (remove emoji and colon)
                role_line = lines[0]
                role = re.sub(r'[🎨⚡🤖☁️💾🎯🔍📊🛡️📱🌐]\s*', '', role_line).replace(':', '').strip()
                
                tasks = []
                for line in lines[1:]:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('---'):
                        # Clean up task formatting
                        task = re.sub(r'^[-•*\d+\.\)]\s*', '', line).strip()
                        task = re.sub(r'^[▶️✨🔧⭐🚀💡🎯🔥]\s*', '', task).strip()
                        
                        if task and len(task) > 10:  # Filter out very short/empty tasks
                            tasks.append(task)
                
                if tasks and len(tasks) >= 2:  # Only include roles with meaningful tasks
                    roles_tasks[role] = tasks
        
        return roles_tasks

class IntelligentRoleSelector:
    """Selects relevant roles based on project keywords and requirements"""
    
    ROLE_KEYWORDS = {
        'Frontend Developer': {
            'keywords': ['ui', 'frontend', 'react', 'vue', 'angular', 'web interface', 'dashboard', 'user interface', 'responsive', 'mobile app', 'ios', 'android'],
            'emoji': '🎨'
        },
        'Backend Developer': {
            'keywords': ['api', 'backend', 'server', 'database', 'authentication', 'microservices', 'rest', 'graphql', 'node', 'python', 'java'],
            'emoji': '⚡'
        },
        'AI/ML Engineer': {
            'keywords': ['ai', 'machine learning', 'ml', 'deep learning', 'nlp', 'computer vision', 'neural network', 'tensorflow', 'pytorch', 'model'],
            'emoji': '🤖'
        },
        'Cloud & DevOps Engineer': {
            'keywords': ['cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd', 'deployment', 'infrastructure', 'devops', 'scalability'],
            'emoji': '☁️'
        },
        'Data Engineer': {
            'keywords': ['data pipeline', 'etl', 'big data', 'data warehouse', 'analytics', 'kafka', 'spark', 'airflow', 'data processing'],
            'emoji': '💾'
        },
        'UI/UX Designer': {
            'keywords': ['design', 'user experience', 'ux', 'ui design', 'wireframe', 'prototype', 'figma', 'user journey', 'branding'],
            'emoji': '🎯'
        },
        'QA Engineer': {
            'keywords': ['testing', 'qa', 'quality assurance', 'automation testing', 'selenium', 'test cases', 'bug tracking'],
            'emoji': '🔍'
        },
        'Data Scientist': {
            'keywords': ['data analysis', 'statistics', 'predictive modeling', 'data visualization', 'insights', 'research', 'jupyter'],
            'emoji': '📊'
        },
        'Security Engineer': {
            'keywords': ['security', 'cybersecurity', 'encryption', 'authentication', 'compliance', 'penetration testing', 'vulnerability'],
            'emoji': '🛡️'
        },
        'Mobile Developer': {
            'keywords': ['mobile', 'ios', 'android', 'react native', 'flutter', 'swift', 'kotlin', 'mobile app'],
            'emoji': '📱'
        },
        'Blockchain Developer': {
            'keywords': ['blockchain', 'cryptocurrency', 'smart contracts', 'ethereum', 'web3', 'defi', 'nft'],
            'emoji': '🌐'
        }
    }
    
    def select_relevant_roles(self, project_description: str) -> List[str]:
        """Select roles based on project requirements"""
        project_lower = project_description.lower()
        relevant_roles = []
        
        for role, data in self.ROLE_KEYWORDS.items():
            # Check if any keywords match
            if any(keyword in project_lower for keyword in data['keywords']):
                relevant_roles.append(role)
        
        # Always include core roles for most projects
        core_roles = ['Frontend Developer', 'Backend Developer']
        for role in core_roles:
            if role not in relevant_roles and any(term in project_lower for term in ['web', 'app', 'platform', 'system', 'full stack']):
                relevant_roles.append(role)
        
        # Add AI/ML Engineer for AI-related projects
        if any(term in project_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'intelligent']):
            if 'AI/ML Engineer' not in relevant_roles:
                relevant_roles.append('AI/ML Engineer')
        
        return relevant_roles

class CreativeProjectBreakdownAgent:
    """Enhanced AI Agent with creative prompts and intelligent role selection"""
    
    def __init__(self, openai_api_key: str):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.llm = ChatOpenAI(temperature=0.8, max_tokens=2000)  # Reduced to fit context limits
        self.parser = SmartProjectTaskParser()
        self.role_selector = IntelligentRoleSelector()
        self._setup_creative_prompt()
    
    def _setup_creative_prompt(self):
        """Setup an enhanced, creative prompt template"""
        
        template = """
🚀 PROJECT ARCHITECT & TASK STRATEGIST 🚀

You are an elite project architect. Break down this project into actionable tasks for each relevant role.

PROJECT: {project_idea}
RELEVANT ROLES: {selected_roles}

OUTPUT FORMAT (use EXACTLY this format):

🎨 Frontend Developer:
▶️ [Specific actionable task with technical details - mention specific frameworks/libraries]
✨ [Another concrete task that sounds exciting and innovative]
🔧 [Implementation-focused task with technical depth]
⭐ [Integration or collaboration task]
🚀 [Advanced/optimization task for performance/scalability]

⚡ Backend Developer:
▶️ [Architecture and API design task with specific technologies]
✨ [Authentication/security implementation task]
🔧 [Database design and optimization task]
⭐ [API documentation and integration task]
🚀 [Performance optimization and scalability task]

🤖 AI/ML Engineer:
▶️ [ML model development task with specific algorithms]
✨ [AI feature implementation with practical applications]
🔧 [Data preprocessing and pipeline task]
⭐ [Model integration with backend services]
🚀 [MLOps and model monitoring task]

☁️ Cloud & DevOps Engineer:
▶️ [Cloud infrastructure design with specific platforms]
✨ [CI/CD pipeline setup with automation tools]
🔧 [Containerization and orchestration task]
⭐ [Monitoring and logging implementation]
🚀 [Cost optimization and scaling strategies]

💾 Data Engineer:
▶️ [ETL pipeline design with specific tools]
✨ [Real-time data streaming implementation]
🔧 [Data lake/warehouse architecture]
⭐ [Data quality and validation frameworks]
🚀 [Data governance and analytics platform]

🎯 UI/UX Designer:
▶️ [User research and persona development]
✨ [Information architecture and user journey design]
🔧 [High-fidelity mockups and prototyping]
⭐ [Developer collaboration for implementation]
🚀 [Usability testing and optimization]



⚡ **TASK CREATION GUIDELINES:**
1. Each task must be specific, measurable, and exciting
2. Include concrete technologies and frameworks (React 18, TensorFlow, Apache Kafka, etc.)
3. Focus on practical implementation with technical depth
4. Consider integration points between different roles
5. Balance foundational work with innovative features
6. Make tasks sound like exciting challenges, not boring chores
7. Include both technical complexity and clear business value
8. Only create tasks for roles that are genuinely needed for this specific project
9. Each task should be 15-25 words for optimal readability
10. Progressive complexity: ▶️ (foundation) → ✨ (features) → 🔧 (implementation) → ⭐ (integration) → 🚀 (optimization)

🎯 **REMEMBER:** Create a roadmap for building something extraordinary that teams will be excited to work on!
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_idea", "selected_roles"],
            template=template
        )
    
    def breakdown_project(self, project_idea: str) -> Dict[str, List[str]]:
        """Break down project with intelligent role selection"""
        
        # Select relevant roles
        relevant_roles = self.role_selector.select_relevant_roles(project_idea)
        
        if not relevant_roles:
            relevant_roles = ['Frontend Developer', 'Backend Developer']  # Fallback
        
        # Create role string with emojis
        role_strings = []
        for role in relevant_roles:
            emoji = self.role_selector.ROLE_KEYWORDS.get(role, {}).get('emoji', '🔸')
            role_strings.append(f"{emoji} {role}")
        
        selected_roles_str = ", ".join(role_strings)
        
        try:
            # Generate the breakdown using new syntax
            chain = self.prompt | self.llm
            result = chain.invoke({
                "project_idea": project_idea,
                "selected_roles": selected_roles_str
            })
            
            # Parse and return
            parsed_result = self.parser.parse(result.content)
            return parsed_result
            
        except Exception as e:
            print(f"Error processing project breakdown: {str(e)}")
            return {}
    
    def format_output(self, tasks_dict: Dict[str, List[str]], project_name: str = "") -> str:
        """Enhanced formatting with creative styling matching the sample output"""
        
        output = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🚀 PROJECT BLUEPRINT 🚀                       ║
║                                                                  ║
║  {project_name.center(60)}  ║
╚══════════════════════════════════════════════════════════════════╝

🎯 **ROLES & RESPONSIBILITIES BREAKDOWN**
══════════════════════════════════════════════════════════════════════
"""
        
        role_emojis = {
            'Frontend Developer': '🎨',
            'Backend Developer': '⚡',
            'AI/ML Engineer': '🤖',
            'Cloud & DevOps Engineer': '☁️',
            'Data Engineer': '💾',
            'UI/UX Designer': '🎯',
            'QA Engineer': '🔍',
            'Data Scientist': '📊',
            'Security Engineer': '🛡️',
            'Mobile Developer': '📱',
            'Blockchain Developer': '🌐'
        }
        
        task_emojis = ['▶️', '✨', '🔧', '⭐', '🚀']
        
        for i, (role, tasks) in enumerate(tasks_dict.items(), 1):
            emoji = role_emojis.get(role, '🔸')
            
            output += f"\n{emoji} **{role.upper()}**\n"
            output += "─" * (len(role) + 15) + "\n"
            
            for j, task in enumerate(tasks):
                task_emoji = task_emojis[j] if j < len(task_emojis) else '💡'
                output += f"{task_emoji} {task}\n"
            
            if i < len(tasks_dict):
                output += "\n" + "┈" * 70 + "\n"
        
        output += f"\n\n🎊 **PROJECT SUMMARY**\n"
        output += f"📋 Total Roles: {len(tasks_dict)}\n"
        output += f"✅ Total Tasks: {sum(len(tasks) for tasks in tasks_dict.values())}\n"
        output += f"🚀 Ready to build something amazing!\n"
        
        return output
    
    def save_breakdown(self, tasks_dict: Dict[str, List[str]], project_name: str, filename: str = None):
        """Save with enhanced metadata"""
        
        if not filename:
            safe_name = re.sub(r'[^\w\s-]', '', project_name).strip()
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            filename = f"{safe_name}_breakdown.json"
        
        breakdown_data = {
            "project_name": project_name,
            "total_roles": len(tasks_dict),
            "total_tasks": sum(len(tasks) for tasks in tasks_dict.values()),
            "roles_and_tasks": tasks_dict,
            "generated_at": "2025-05-31"  # You could use datetime here
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(breakdown_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Project breakdown saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")

def main():
    """Interactive main function with enhanced UX"""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║               🤖 CREATIVE PROJECT BREAKDOWN AGENT 🤖              ║
║                                                                  ║
║        Transform your ideas into actionable roadmaps!           ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    api_key = input("🔑 Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ OpenAI API key is required!")
        return
    
    agent = CreativeProjectBreakdownAgent(api_key)
    
    while True:
        print("\n" + "═" * 70)
        project_idea = input("💡 Describe your project idea (or 'quit' to exit): ").strip()
        
        if project_idea.lower() in ['quit', 'exit', 'q']:
            print("🎉 Thanks for using the Creative Project Breakdown Agent! Build something amazing! 🚀")
            break
        
        if not project_idea:
            print("❌ Please enter a valid project idea!")
            continue
        
        print("\n🔄 Analyzing your project and selecting relevant roles...")
        print("🧠 Generating creative task breakdown...")
        
        tasks = agent.breakdown_project(project_idea)
        
        if tasks:
            formatted_output = agent.format_output(tasks, project_idea)
            print(formatted_output)
            
            save_choice = input("\n💾 Save this breakdown? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                agent.save_breakdown(tasks, project_idea)
        else:
            print("❌ Failed to process the project idea. Please try again with more details.")

if __name__ == "__main__":
    main()