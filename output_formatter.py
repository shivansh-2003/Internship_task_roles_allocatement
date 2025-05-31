import re
import json
from typing import Dict, List

class OutputFormatter:
    """Formats project breakdown output into clean JSON structure"""
    
    def parse_formatted_output(self, formatted_text: str) -> Dict[str, Dict[str, List[str]]]:
        """
        Parse the formatted output into JSON structure
        
        Args:
            formatted_text (str): The formatted output from the breakdown agent
            
        Returns:
            Dict: Clean JSON structure with roles and responsibilities
        """
        
        # Extract project name from the header
        project_name = self._extract_project_name(formatted_text)
        
        # Parse roles and tasks
        roles_data = self._parse_roles_and_tasks(formatted_text)
        
        # Create final JSON structure
        result = {
            "project_name": project_name,
            "roles_and_responsibilities": roles_data,
            "summary": {
                "total_roles": len(roles_data),
                "total_tasks": sum(len(tasks) for tasks in roles_data.values())
            }
        }
        
        return result
    
    def _extract_project_name(self, text: str) -> str:
        """Extract project name from the formatted header"""
        # Look for text in the center of the PROJECT BLUEPRINT section
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'PROJECT BLUEPRINT' in line:
                # Look for the project name in the next few lines
                for j in range(i+1, min(i+4, len(lines))):
                    if lines[j].strip() and not any(char in lines[j] for char in ['=', '-', '*']):
                        project_name = lines[j].strip()
                        if project_name and len(project_name) > 3:
                            return project_name
        return "Unknown Project"
    
    def _parse_roles_and_tasks(self, text: str) -> Dict[str, List[str]]:
        """Parse roles and their associated tasks"""
        roles_data = {}
        
        # Split text into lines
        lines = text.split('\n')
        current_role = None
        current_tasks = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and separators
            if not line or line.startswith('=') or line.startswith('-') or line.startswith('.'):
                continue
                
            # Check if this is a role header (all caps and followed by dashes in next lines)
            if line.startswith('**') and line.endswith('**') and line.isupper():
                # Save previous role if exists
                if current_role and current_tasks:
                    roles_data[current_role] = current_tasks.copy()
                
                # Start new role
                current_role = line.replace('**', '').strip()
                current_tasks = []
                continue
            
            # Check if this is a task (starts with number)
            task_match = re.match(r'^\d+\.\s*(.+)', line)
            if task_match and current_role:
                task_text = task_match.group(1).strip()
                if len(task_text) > 10:  # Only include meaningful tasks
                    current_tasks.append(task_text)
        
        # Don't forget the last role
        if current_role and current_tasks:
            roles_data[current_role] = current_tasks
        
        return roles_data
    
    def format_to_json(self, formatted_text: str, pretty_print: bool = True) -> str:
        """
        Convert formatted output to JSON string
        
        Args:
            formatted_text (str): The formatted output
            pretty_print (bool): Whether to format JSON with indentation
            
        Returns:
            str: JSON formatted string
        """
        parsed_data = self.parse_formatted_output(formatted_text)
        
        if pretty_print:
            return json.dumps(parsed_data, indent=2, ensure_ascii=False)
        else:
            return json.dumps(parsed_data, ensure_ascii=False)
    