import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI

class GPTUniversityEnhancer:
    def __init__(self):
        """
        Initialize the GPT University Enhancer with OpenRouter configuration
        """
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key")
        )
        self.model = "openai/gpt-3.5-turbo"
    
    async def generate_university_data(self, university_name: str, country: str, field: str = "Computer Science") -> Optional[Dict[str, Any]]:
        """
        Generate comprehensive university data using GPT
        """
        try:
            prompt = f"""
            Generate comprehensive data for {university_name} in {country} for {field} studies.
            
            Return a JSON object with the following structure:
            {{
                "name": "{university_name}",
                "country": "{country}",
                "ranking": <global ranking number>,
                "tuition_fee": "<annual fee in USD>",
                "scholarship_available": <true/false>,
                "program_name": "{field} Program",
                "duration": "<program duration>",
                "requirements": "<admission requirements>",
                "research_areas": ["<area1>", "<area2>", "<area3>"],
                "faculty_highlights": "<notable faculty information>",
                "campus_life": "<campus life description>",
                "application_deadline": "<deadline>",
                "website": "<university website>",
                "description": "<university description>",
                "strengths": ["<strength1>", "<strength2>", "<strength3>"],
                "admission_rate": "<percentage>"
            }}
            
            Make the data realistic and comprehensive.
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a university data expert. Generate accurate and comprehensive university information in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            # Extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            
            return None
            
        except Exception as e:
            print(f"Error generating university data: {e}")
            return None
    
    async def enhance_existing_university(self, university_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance existing university data with additional AI-generated information
        """
        try:
            prompt = f"""
            Enhance the following university data with more detailed and comprehensive information:
            
            Current data: {json.dumps(university_data, indent=2)}
            
            Add or improve the following fields if missing or incomplete:
            - research_areas (list of 3-5 areas)
            - faculty_highlights
            - campus_life
            - strengths (list of 3-5 strengths)
            - description (comprehensive description)
            
            Return the enhanced data as a complete JSON object with all original fields plus improvements.
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a university data expert. Enhance university information while preserving existing accurate data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200
            )
            
            content = response.choices[0].message.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                enhanced_data = json.loads(json_str)
                return enhanced_data
            
            return university_data
            
        except Exception as e:
            print(f"Error enhancing university data: {e}")
            return university_data
    
    async def generate_university_list(self, field: str, country: str = None, count: int = 5) -> List[Dict[str, str]]:
        """
        Generate a list of top universities for a specific field
        """
        try:
            location_filter = f" in {country}" if country else " worldwide"
            
            prompt = f"""
            Generate a list of the top {count} universities for {field} studies{location_filter}.
            
            Return a JSON array with the following structure:
            [
                {{
                    "name": "<university name>",
                    "country": "<country>",
                    "ranking": <global ranking for this field>
                }},
                ...
            ]
            
            Focus on universities with strong {field} programs.
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a university ranking expert. Provide accurate university rankings for specific fields."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            
            return []
            
        except Exception as e:
            print(f"Error generating university list: {e}")
            return []
    
    async def generate_program_details(self, university_name: str, program_name: str) -> Optional[Dict[str, Any]]:
        """
        Generate detailed information about a specific program at a university
        """
        try:
            prompt = f"""
            Generate detailed information about the {program_name} program at {university_name}.
            
            Return a JSON object with the following structure:
            {{
                "university_name": "{university_name}",
                "program_name": "{program_name}",
                "degree_type": "<Bachelor's/Master's/PhD>",
                "duration": "<program duration>",
                "curriculum": ["<course1>", "<course2>", "<course3>"],
                "specializations": ["<spec1>", "<spec2>"],
                "admission_requirements": "<requirements>",
                "career_prospects": ["<career1>", "<career2>", "<career3>"],
                "tuition_fee": "<annual fee>",
                "application_deadline": "<deadline>",
                "contact_info": "<contact information>"
            }}
            
            Make the information comprehensive and realistic.
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an academic program expert. Generate detailed and accurate program information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            
            return None
            
        except Exception as e:
            print(f"Error generating program details: {e}")
            return None