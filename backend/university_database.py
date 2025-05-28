import csv
import asyncio
import json
import requests
import os
from datetime import datetime
from typing import List, Dict, Any
from gpt_university_enhancer import GPTUniversityEnhancer

class UniversityDatabase:
    """
    University database class that manages university data
    In production, this would connect to a real database
    """
    
    def __init__(self):
        try:
            self.universities = []
            self.gpt_enhancer = GPTUniversityEnhancer()
            
            # Load universities from CSV file
            csv_universities = self._load_universities_from_csv()
            self.universities.extend(csv_universities)
            
            # Load US universities from College Scorecard API
            us_universities = self._fetch_us_universities()
            self.universities.extend(us_universities)
            
            # If no universities loaded, use minimal fallback
            if not self.universities:
                print("No universities loaded, using minimal fallback data")
                self.universities = self._get_minimal_fallback_data()
        except Exception as e:
            print(f"Error initializing university database: {e}")
            self.universities = self._get_minimal_fallback_data()
            self.gpt_enhancer = GPTUniversityEnhancer()
    
    def _load_universities_from_csv(self) -> List[Dict[str, Any]]:
        """
        Load university data from the world-universities.csv file
        """
        universities = []
        csv_file_path = "/Users/wisemaker/Sites/university-recommender/backend/world-universities.csv"
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                
                for idx, row in enumerate(csv_reader):
                    if len(row) >= 3:  # Ensure we have country, name, and website
                        country_code = row[0].strip()
                        university_name = row[1].strip()
                        website = row[2].strip() if len(row) > 2 else ""
                        
                        # Convert country code to full country name
                        country_name = self._get_country_name(country_code)
                        
                        university_data = {
                            "id": idx + 1,
                            "name": university_name,
                            "country": country_name,
                            "country_code": country_code,
                            "website": website,
                            "ranking": None,  # Will be populated by AI if needed
                            "match_score": 75,  # Default score
                            "tuition_fee": "Contact university for details",
                            "scholarship_available": True,
                            "program_name": "Various programs available",
                            "duration": "Varies by program",
                            "requirements": ["Contact university for specific requirements"],
                            "research_areas": ["Multiple disciplines"],
                            "faculty_highlights": [],
                            "campus_life": "Contact university for campus information",
                            "application_deadline": "Varies by program",
                            "description": f"University located in {country_name}",
                            "strengths": ["Academic Excellence"],
                            "admission_rate": "Contact university for details"
                        }
                        
                        universities.append(university_data)
                        
            print(f"Loaded {len(universities)} universities from CSV file")
            return universities
            
        except FileNotFoundError:
            print(f"CSV file not found at {csv_file_path}")
            return []
        except Exception as e:
            print(f"Error loading universities from CSV: {e}")
            return []
    
    def _get_country_name(self, country_code: str) -> str:
        """
        Convert country code to full country name
        """
        country_mapping = {
            "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan", "AG": "Antigua and Barbuda",
            "AI": "Anguilla", "AL": "Albania", "AM": "Armenia", "AO": "Angola", "AQ": "Antarctica",
            "AR": "Argentina", "AS": "American Samoa", "AT": "Austria", "AU": "Australia", "AW": "Aruba",
            "AX": "Åland Islands", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
            "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain",
            "BI": "Burundi", "BJ": "Benin", "BL": "Saint Barthélemy", "BM": "Bermuda", "BN": "Brunei",
            "BO": "Bolivia", "BQ": "Caribbean Netherlands", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan",
            "BV": "Bouvet Island", "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada",
            "CC": "Cocos Islands", "CD": "Democratic Republic of the Congo", "CF": "Central African Republic",
            "CG": "Republic of the Congo", "CH": "Switzerland", "CI": "Côte d'Ivoire", "CK": "Cook Islands",
            "CL": "Chile", "CM": "Cameroon", "CN": "China", "CO": "Colombia", "CR": "Costa Rica",
            "CU": "Cuba", "CV": "Cape Verde", "CW": "Curaçao", "CX": "Christmas Island", "CY": "Cyprus",
            "CZ": "Czech Republic", "DE": "Germany", "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica",
            "DO": "Dominican Republic", "DZ": "Algeria", "EC": "Ecuador", "EE": "Estonia", "EG": "Egypt",
            "EH": "Western Sahara", "ER": "Eritrea", "ES": "Spain", "ET": "Ethiopia", "FI": "Finland",
            "FJ": "Fiji", "FK": "Falkland Islands", "FM": "Micronesia", "FO": "Faroe Islands", "FR": "France",
            "GA": "Gabon", "GB": "United Kingdom", "GD": "Grenada", "GE": "Georgia", "GF": "French Guiana",
            "GG": "Guernsey", "GH": "Ghana", "GI": "Gibraltar", "GL": "Greenland", "GM": "Gambia",
            "GN": "Guinea", "GP": "Guadeloupe", "GQ": "Equatorial Guinea", "GR": "Greece",
            "GS": "South Georgia and the South Sandwich Islands", "GT": "Guatemala", "GU": "Guam",
            "GW": "Guinea-Bissau", "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island and McDonald Islands",
            "HN": "Honduras", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia",
            "IE": "Ireland", "IL": "Israel", "IM": "Isle of Man", "IN": "India", "IO": "British Indian Ocean Territory",
            "IQ": "Iraq", "IR": "Iran", "IS": "Iceland", "IT": "Italy", "JE": "Jersey", "JM": "Jamaica",
            "JO": "Jordan", "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KH": "Cambodia",
            "KI": "Kiribati", "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "North Korea",
            "KR": "South Korea", "KW": "Kuwait", "KY": "Cayman Islands", "KZ": "Kazakhstan", "LA": "Laos",
            "LB": "Lebanon", "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia",
            "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya",
            "MA": "Morocco", "MC": "Monaco", "MD": "Moldova", "ME": "Montenegro", "MF": "Saint Martin",
            "MG": "Madagascar", "MH": "Marshall Islands", "MK": "North Macedonia", "ML": "Mali",
            "MM": "Myanmar", "MN": "Mongolia", "MO": "Macao", "MP": "Northern Mariana Islands",
            "MQ": "Martinique", "MR": "Mauritania", "MS": "Montserrat", "MT": "Malta", "MU": "Mauritius",
            "MV": "Maldives", "MW": "Malawi", "MX": "Mexico", "MY": "Malaysia", "MZ": "Mozambique",
            "NA": "Namibia", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria",
            "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NP": "Nepal", "NR": "Nauru",
            "NU": "Niue", "NZ": "New Zealand", "OM": "Oman", "PA": "Panama", "PE": "Peru",
            "PF": "French Polynesia", "PG": "Papua New Guinea", "PH": "Philippines", "PK": "Pakistan",
            "PL": "Poland", "PM": "Saint Pierre and Miquelon", "PN": "Pitcairn", "PR": "Puerto Rico",
            "PS": "Palestine", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay", "QA": "Qatar",
            "RE": "Réunion", "RO": "Romania", "RS": "Serbia", "RU": "Russia", "RW": "Rwanda",
            "SA": "Saudi Arabia", "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan",
            "SE": "Sweden", "SG": "Singapore", "SH": "Saint Helena", "SI": "Slovenia", "SJ": "Svalbard and Jan Mayen",
            "SK": "Slovakia", "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal", "SO": "Somalia",
            "SR": "Suriname", "SS": "South Sudan", "ST": "São Tomé and Príncipe", "SV": "El Salvador",
            "SX": "Sint Maarten", "SY": "Syria", "SZ": "Eswatini", "TC": "Turks and Caicos Islands",
            "TD": "Chad", "TF": "French Southern Territories", "TG": "Togo", "TH": "Thailand",
            "TJ": "Tajikistan", "TK": "Tokelau", "TL": "Timor-Leste", "TM": "Turkmenistan", "TN": "Tunisia",
            "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago", "TV": "Tuvalu", "TW": "Taiwan",
            "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda", "UM": "United States Minor Outlying Islands",
            "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan", "VA": "Vatican City",
            "VC": "Saint Vincent and the Grenadines", "VE": "Venezuela", "VG": "British Virgin Islands",
            "VI": "U.S. Virgin Islands", "VN": "Vietnam", "VU": "Vanuatu", "WF": "Wallis and Futuna",
            "WS": "Samoa", "YE": "Yemen", "YT": "Mayotte", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe"
        }
        return country_mapping.get(country_code, country_code)
    
    def _fetch_us_universities(self) -> List[Dict[str, Any]]:
        """
        Fetch US university data from College Scorecard API
        """
        try:
            # Get API key from environment variable
            api_key = os.getenv('COLLEGE_SCORECARD_API_KEY')
            if not api_key:
                print("Warning: COLLEGE_SCORECARD_API_KEY not found. Skipping US universities.")
                return []
            
            # Fetch top universities from College Scorecard API
            url = "https://api.data.gov/ed/collegescorecard/v1/schools"
            params = {
                'api_key': api_key,
                'fields': 'school.name,school.state,school.city,latest.admissions.admission_rate.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state',
                'latest.academics.program_available.assoc_or_bachelors': 'true',
                'per_page': 100
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                universities = []
                
                for idx, school in enumerate(data.get('results', [])):
                    if school.get('school.name'):
                        university_data = {
                            "id": len(self.universities) + idx + 1,
                            "name": school['school.name'],
                            "country": "United States",
                            "state": school.get('school.state', ''),
                            "city": school.get('school.city', ''),
                            "ranking": None,
                            "match_score": 80,
                            "tuition_fee": f"${school.get('latest.cost.tuition.out_of_state', 'N/A')}/year (Out-of-state)",
                            "scholarship_available": True,
                            "program_name": "Various programs available",
                            "duration": "Varies by program",
                            "requirements": ["Contact university for specific requirements"],
                            "research_areas": ["Multiple disciplines"],
                            "faculty_highlights": [],
                            "campus_life": "Contact university for campus information",
                            "application_deadline": "Varies by program",
                            "website": "",
                            "description": f"University located in {school.get('school.city', '')}, {school.get('school.state', '')}",
                            "strengths": ["Academic Excellence"],
                            "admission_rate": f"{school.get('latest.admissions.admission_rate.overall', 'N/A')}" if school.get('latest.admissions.admission_rate.overall') else "Contact university for details"
                        }
                        universities.append(university_data)
                
                print(f"Loaded {len(universities)} US universities from College Scorecard API")
                return universities
            else:
                print(f"Failed to fetch US universities: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error fetching US universities: {e}")
            return []
    
    def _get_minimal_fallback_data(self) -> List[Dict[str, Any]]:
        """
        Minimal fallback data if all other sources fail
        """
        return [
            {
                "id": 1,
                "name": "Harvard University",
                "country": "United States",
                "ranking": 1,
                "match_score": 95,
                "tuition_fee": "$54,002/year",
                "scholarship_available": True,
                "program_name": "Various programs available",
                "duration": "Varies by program",
                "requirements": ["Contact university for specific requirements"],
                "research_areas": ["Multiple disciplines"],
                "faculty_highlights": [],
                "campus_life": "Historic campus with world-class facilities",
                "application_deadline": "Varies by program",
                "website": "https://www.harvard.edu",
                "description": "One of the world's leading universities",
                "strengths": ["Academic Excellence", "Research Leadership", "Global Recognition"],
                "admission_rate": "3.4%"
            }
        ]
    
    async def get_all_universities(self) -> List[Dict[str, Any]]:
        """
        Get all universities from the database
        """
        # Simulate async database operation
        await asyncio.sleep(0.1)
        return self.universities.copy()
    
    async def get_university_by_id(self, university_id: int) -> Dict[str, Any]:
        """
        Get a specific university by ID
        """
        await asyncio.sleep(0.1)
        for uni in self.universities:
            if uni["id"] == university_id:
                return uni.copy()
        return None
    
    async def search_universities(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search universities by name, country, or other criteria
        """
        await asyncio.sleep(0.1)
        
        query = query.lower()
        results = []
        
        for uni in self.universities:
            # Search in name, country, and research areas
            searchable_text = (
                uni["name"].lower() + " " +
                uni["country"].lower() + " " +
                " ".join(uni["research_areas"]).lower() + " " +
                uni["program_name"].lower()
            )
            
            if query in searchable_text:
                results.append(uni.copy())
            
            if len(results) >= limit:
                break
        
        return results
    
    async def filter_universities(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter universities based on criteria
        """
        await asyncio.sleep(0.1)
        
        filtered = self.universities.copy()
        
        # Filter by country
        if filters.get("country"):
            country = filters["country"].lower()
            filtered = [uni for uni in filtered if country in uni["country"].lower()]
        
        # Filter by ranking (top N)
        if filters.get("max_ranking"):
            max_rank = filters["max_ranking"]
            filtered = [uni for uni in filtered if uni.get("ranking") and uni["ranking"] <= max_rank]
        
        # Filter by scholarship availability
        if filters.get("scholarship_required"):
            filtered = [uni for uni in filtered if uni["scholarship_available"]]
        
        # Filter by research area
        if filters.get("research_area"):
            research_area = filters["research_area"].lower()
            filtered = [uni for uni in filtered 
                       if any(research_area in area.lower() for area in uni["research_areas"])]
        
        return filtered
    
    async def add_university(self, university_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new university to the database
        """
        await asyncio.sleep(0.1)
        
        # Generate new ID
        new_id = max([uni["id"] for uni in self.universities]) + 1
        university_data["id"] = new_id
        
        self.universities.append(university_data)
        return university_data
    
    async def update_university(self, university_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing university
        """
        await asyncio.sleep(0.1)
        
        for i, uni in enumerate(self.universities):
            if uni["id"] == university_id:
                self.universities[i].update(update_data)
                return self.universities[i].copy()
        
        return None
    
    async def delete_university(self, university_id: int) -> bool:
        """
        Delete a university from the database
        """
        await asyncio.sleep(0.1)
        
        for i, uni in enumerate(self.universities):
            if uni["id"] == university_id:
                del self.universities[i]
                return True
        
        return False
    
    async def generate_universities_for_field(self, field: str, country: str = None, count: int = 3) -> List[Dict[str, Any]]:
        """
        Generate top universities for a specific field using AI
        """
        try:
            # Get university list from GPT
            university_list = await self.gpt_enhancer.generate_university_list(field, country, count)
            
            # Generate detailed data for each university
            detailed_universities = []
            for uni_info in university_list:
                detailed_data = await self.gpt_enhancer.generate_university_data(
                    uni_info["name"], 
                    uni_info["country"], 
                    field
                )
                if detailed_data:
                    detailed_universities.append(detailed_data)
            
            return detailed_universities[:count]
            
        except Exception as e:
            print(f"Error generating universities for field {field}: {e}")
            # Fallback to existing data if available
            return await self.search_universities(field, count)
    
    async def generate_university_with_gpt(self, university_name: str, country: str, field: str = "Computer Science") -> Dict[str, Any]:
        """
        Generate comprehensive university data using GPT
        """
        try:
            return await self.gpt_enhancer.generate_university_data(university_name, country, field)
        except Exception as e:
            print(f"Error generating university data for {university_name}: {e}")
            return None
