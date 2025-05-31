import os
import re
from typing import Dict, List, Tuple, Set
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv
import json

load_dotenv()

class RoleAnalysisParser(BaseOutputParser):
    """Parser to extract role analysis and selections from AI response"""
    
    def parse(self, text: str) -> Dict[str, any]:
        """Parse the AI response to extract roles and reasoning"""
        
        # Initialize result structure
        result = {
            "selected_roles": [],
            "reasoning": "",
            "project_type": "",
            "complexity": "medium"
        }
        
        lines = text.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Identify sections
            if "SELECTED ROLES:" in line.upper():
                current_section = "roles"
                continue
            elif "REASONING:" in line.upper() or "ANALYSIS:" in line.upper():
                current_section = "reasoning"
                continue
            elif "PROJECT TYPE:" in line.upper():
                current_section = "project_type"
                continue
            elif "COMPLEXITY:" in line.upper():
                current_section = "complexity"
                continue
            
            # Process based on current section
            if current_section == "roles":
                # Extract role from numbered or bulleted list
                role_match = re.match(r'^[\d+\.\-\*\•]\s*(.+)', line)
                if role_match:
                    role = role_match.group(1).strip()
                    # Clean up any extra formatting
                    role = re.sub(r'^[:\-\s]+', '', role).strip()
                    if len(role) > 3:
                        result["selected_roles"].append(role)
                elif line and not any(char in line for char in ['=', '-', '*']) and len(line.split()) <= 4:
                    # Simple role name on its own line
                    result["selected_roles"].append(line)
            
            elif current_section == "reasoning":
                result["reasoning"] += line + " "
            elif current_section == "project_type":
                result["project_type"] = line
            elif current_section == "complexity":
                result["complexity"] = line.lower()
        
        return result

class IntelligentRoleAgent:
    """Advanced role selection agent that analyzes projects and selects optimal team roles"""
    
    # Comprehensive role taxonomy organized by expertise areas
    ROLE_TAXONOMY = {
        'Frontend Development': {
            'Web Frontend Developer': {
                'keywords': ['web', 'frontend', 'react', 'vue', 'angular', 'javascript', 'ui', 'interface', 'responsive'],
                'complexity_weight': 2
            },
            'Mobile Frontend Developer': {
                'keywords': ['mobile', 'ios', 'android', 'react native', 'flutter', 'swift', 'kotlin', 'app'],
                'complexity_weight': 3
            },
            'Desktop Application Developer': {
                'keywords': ['desktop', 'electron', 'native', 'windows', 'mac', 'linux', 'qt'],
                'complexity_weight': 3
            }
        },
        'Backend Development': {
            'Backend Developer': {
                'keywords': ['backend', 'api', 'server', 'database', 'microservices', 'rest', 'graphql'],
                'complexity_weight': 2
            },
            'Database Specialist': {
                'keywords': ['database', 'sql', 'nosql', 'data modeling', 'optimization', 'dba'],
                'complexity_weight': 3
            },
            'API Architect': {
                'keywords': ['api design', 'microservices', 'distributed systems', 'scalability'],
                'complexity_weight': 4
            }
        },
        'AI & Machine Learning': {
            'AI/ML Engineer': {
                'keywords': ['ai', 'machine learning', 'ml', 'neural networks', 'deep learning', 'tensorflow', 'pytorch'],
                'complexity_weight': 4
            },
            'Data Scientist': {
                'keywords': ['data science', 'analytics', 'statistics', 'insights', 'modeling', 'research'],
                'complexity_weight': 3
            },
            'NLP Engineer': {
                'keywords': ['nlp', 'natural language', 'text processing', 'chatbot', 'language model'],
                'complexity_weight': 4
            },
            'Computer Vision Engineer': {
                'keywords': ['computer vision', 'image processing', 'object detection', 'facial recognition'],
                'complexity_weight': 4
            }
        },
        'Data Engineering': {
            'Data Engineer': {
                'keywords': ['data pipeline', 'etl', 'data warehouse', 'big data', 'kafka', 'spark', 'airflow'],
                'complexity_weight': 3
            },
            'MLOps Engineer': {
                'keywords': ['mlops', 'model deployment', 'ml pipeline', 'model monitoring', 'kubeflow'],
                'complexity_weight': 4
            }
        },
        'Cloud & Infrastructure': {
            'Cloud Engineer': {
                'keywords': ['cloud', 'aws', 'azure', 'gcp', 'infrastructure', 'terraform', 'kubernetes'],
                'complexity_weight': 3
            },
            'DevOps Engineer': {
                'keywords': ['devops', 'ci/cd', 'deployment', 'automation', 'docker', 'jenkins'],
                'complexity_weight': 3
            },
            'Security Engineer': {
                'keywords': ['security', 'cybersecurity', 'encryption', 'compliance', 'penetration testing'],
                'complexity_weight': 4
            }
        },
        'Design & User Experience': {
            'UI/UX Designer': {
                'keywords': ['ui', 'ux', 'design', 'user experience', 'wireframe', 'prototype', 'figma'],
                'complexity_weight': 2
            },
            'Product Designer': {
                'keywords': ['product design', 'user research', 'design thinking', 'user journey'],
                'complexity_weight': 3
            },
            'Graphic Designer': {
                'keywords': ['graphic design', 'branding', 'visual design', 'illustration'],
                'complexity_weight': 2
            }
        },
        'Quality Assurance': {
            'QA Engineer': {
                'keywords': ['testing', 'qa', 'quality assurance', 'test automation', 'selenium'],
                'complexity_weight': 2
            },
            'Performance Engineer': {
                'keywords': ['performance testing', 'load testing', 'optimization', 'benchmarking'],
                'complexity_weight': 3
            }
        },
        'Specialized Technologies': {
            'Blockchain Developer': {
                'keywords': ['blockchain', 'cryptocurrency', 'smart contracts', 'ethereum', 'web3', 'defi'],
                'complexity_weight': 5
            },
            'IoT Engineer': {
                'keywords': ['iot', 'internet of things', 'embedded', 'sensors', 'hardware'],
                'complexity_weight': 4
            },
            'Game Developer': {
                'keywords': ['game', 'gaming', 'unity', 'unreal', 'game engine'],
                'complexity_weight': 4
            },
            'AR/VR Developer': {
                'keywords': ['ar', 'vr', 'augmented reality', 'virtual reality', 'metaverse'],
                'complexity_weight': 5
            }
        },
        'Management & Strategy': {
            'Technical Project Manager': {
                'keywords': ['project management', 'coordination', 'agile', 'scrum', 'planning'],
                'complexity_weight': 2
            },
            'Product Manager': {
                'keywords': ['product management', 'requirements', 'roadmap', 'stakeholder'],
                'complexity_weight': 2
            },
            'Solution Architect': {
                'keywords': ['architecture', 'system design', 'technical strategy', 'scalability'],
                'complexity_weight': 4
            }
        }
    }
    
    def __init__(self, api_key: str = None):
        """Initialize the role agent with OpenAI API"""
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key is required! Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize LLM with optimized settings for role analysis
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.4,  # Balanced for creativity and consistency
            max_tokens=1500
        )
        
        self.parser = RoleAnalysisParser()
        self._setup_role_selection_prompt()
    
    def _setup_role_selection_prompt(self):
        """Create an intelligent prompt for role selection"""
        
        # Generate available roles text
        roles_text = self._generate_roles_catalog()
        
        template = """
🎯 **INTELLIGENT ROLE SELECTION SPECIALIST**

You are an expert technical architect and team composition specialist. Your task is to analyze project requirements and select the optimal team roles.

📋 **PROJECT TO ANALYZE:**
{project_description}

🏗️ **AVAILABLE ROLES CATALOG:**
{available_roles}

🧠 **ANALYSIS FRAMEWORK:**

1. **Project Type Classification**: Identify if this is a web app, mobile app, AI system, data platform, enterprise software, etc.

2. **Technical Complexity Assessment**: 
   - Simple (2-3 roles): Basic CRUD apps, simple websites
   - Medium (4-5 roles): Complex applications with integrations
   - High (6+ roles): Enterprise systems, AI platforms, complex infrastructures

3. **Core Requirements Analysis**:
   - User interaction needs (Frontend requirements)
   - Data processing needs (Backend/Database requirements)
   - Specialized technology needs (AI, Blockchain, etc.)
   - Deployment and scaling needs (DevOps/Cloud)
   - Quality and security needs (QA, Security)

4. **Team Optimization**:
   - Always include essential roles for the project type
   - Add specialized roles only when genuinely needed
   - Consider project lifecycle (development, testing, deployment)
   - Balance team size with project scope

🎯 **SELECTION CRITERIA:**
- Focus on roles that will have substantial, ongoing work
- Ensure coverage of all critical project aspects
- Avoid redundant or marginally useful roles
- Consider both development and operational phases

📝 **OUTPUT FORMAT:**

PROJECT TYPE: [Web Application/Mobile App/AI System/Data Platform/etc.]

COMPLEXITY: [Simple/Medium/High]

SELECTED ROLES:
1. [Role Name]
2. [Role Name]
3. [Role Name]
4. [Role Name]
5. [Role Name]

REASONING:
[Provide 2-3 sentences explaining why each role is essential for this specific project. Consider the project's unique requirements and how each role contributes to success.]

🔍 **Remember**: Quality over quantity. Better to have 3-5 highly relevant roles than 8 roles where some have minimal contribution.
"""
        
        self.prompt = PromptTemplate(
            input_variables=["project_description", "available_roles"],
            template=template
        )
        self.roles_catalog = roles_text
    
    def _generate_roles_catalog(self) -> str:
        """Generate a formatted catalog of available roles"""
        
        catalog = ""
        for domain, roles in self.ROLE_TAXONOMY.items():
            catalog += f"\n**{domain}:**\n"
            for role_name, role_data in roles.items():
                complexity = "●" * role_data['complexity_weight']
                catalog += f"  • {role_name} {complexity}\n"
        
        return catalog
    
    def analyze_project(self, project_description: str) -> Dict[str, any]:
        """
        Analyze project and return comprehensive role selection with reasoning
        
        Args:
            project_description (str): Description of the project
            
        Returns:
            Dict containing selected roles, reasoning, project type, and complexity
        """
        
        try:
            # Generate role analysis
            chain = self.prompt | self.llm
            result = chain.invoke({
                "project_description": project_description,
                "available_roles": self.roles_catalog
            })
            
            # Parse the response
            analysis = self.parser.parse(result.content)
            
            # Validate and enhance the selection - let AI handle this intelligently
            return analysis
            
        except Exception as e:
            print(f"Error in project analysis: {str(e)}")
            # Fallback analysis
            return {
                "selected_roles": ["Frontend Developer", "Backend Developer"],
                "reasoning": "Fallback selection due to analysis error",
                "project_type": "Web Application",
                "complexity": "medium"
            }
    
    def get_role_recommendations(self, project_description: str) -> Dict[str, any]:
        """Get role recommendations with AI-driven analysis"""
        
        analysis = self.analyze_project(project_description)
        return analysis

def main():
    """Demo the intelligent role agent"""
    
    print("🎯 INTELLIGENT ROLE SELECTION AGENT")
    print("=" * 50)
    
    try:
        # Initialize agent
        agent = IntelligentRoleAgent()
        print("✅ Agent initialized successfully\n")
        
        # Test projects
        test_projects = [
            "An intelligent AI-powered assistant that transforms various content types into engaging LinkedIn blog posts",
            "A mobile fitness tracking app with social features and AI-powered workout recommendations",
            "An enterprise blockchain-based supply chain management platform"
        ]
        
        for i, project in enumerate(test_projects, 1):
            print(f"🚀 Test Project {i}:")
            print(f"Project: {project}\n")
            
            # Get role recommendations
            recommendations = agent.get_role_recommendations(project)
            
            print(f"📊 Analysis Results:")
            print(f"Project Type: {recommendations.get('project_type', 'Unknown')}")
            print(f"Complexity: {recommendations.get('complexity', 'Medium')}")
            
            print(f"\n👥 Selected Roles:")
            for j, role in enumerate(recommendations['selected_roles'], 1):
                print(f"{j}. {role}")
            
            print(f"\n💭 Reasoning:")
            print(f"{recommendations.get('reasoning', 'No reasoning provided')}")
            
            print("\n" + "="*50 + "\n")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenAI API key in the .env file or environment variables")

if __name__ == "__main__":
    main()