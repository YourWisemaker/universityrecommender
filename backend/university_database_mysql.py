import mysql.connector
import asyncio
import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Any, Optional
from gpt_university_enhancer import GPTUniversityEnhancer

# Load environment variables
load_dotenv()

class UniversityDatabaseMySQL:
    def __init__(self):
        """
        Initialize MySQL University Database
        """
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'universitydb')
        }
        self.gpt_enhancer = GPTUniversityEnhancer()
        
    def get_connection(self):
        """Get MySQL database connection"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            return None
    
    def get_all_universities(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all universities with pagination
        """
        conn = self.get_connection()
        if not conn:
            return self._get_minimal_fallback_data()
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT id, country_code, country_name, name, website, global_ranking,
                   tuition_fee_usd, scholarship_available, admission_rate,
                   student_population, founded_year, type, research_areas,
                   campus_size, admission_requirements, notable_faculty, 
                   program_strengths, application_deadline, created_at
            FROM universities 
            ORDER BY COALESCE(global_ranking, 9999), name
            LIMIT %s OFFSET %s
            """
            cursor.execute(query, (limit, offset))
            universities = cursor.fetchall()
            
            # Convert to the expected format
            formatted_universities = []
            for uni in universities:
                # Generate program name based on research areas or default
                research_areas_list = uni['research_areas'].split(', ') if uni['research_areas'] else []
                program_name = research_areas_list[0] if research_areas_list else "General Studies"
                
                # Parse admission requirements into list
                requirements = uni['admission_requirements'].split('; ') if uni['admission_requirements'] else []
                
                # Parse notable faculty into list for faculty highlights
                faculty_highlights = uni['notable_faculty'].split('; ') if uni['notable_faculty'] else []
                
                # Parse program strengths into list
                strengths = uni['program_strengths'].split('; ') if uni['program_strengths'] else []
                
                formatted_uni = {
                    'id': uni['id'],
                    'name': uni['name'],
                    'country': uni['country_name'],
                    'country_code': uni['country_code'],
                    'website': uni['website'],
                    'ranking': uni['global_ranking'],
                    'tuition_fee': uni['tuition_fee_usd'],
                    'scholarship_available': bool(uni['scholarship_available']),
                    'admission_rate': uni['admission_rate'] if uni['admission_rate'] else "Not specified",
                    'student_population': uni['student_population'],
                    'founded_year': uni['founded_year'],
                    'type': uni['type'],
                    'research_areas': research_areas_list,
                    'campus_size': uni['campus_size'],
                    'admission_requirements': uni['admission_requirements'],
                    'notable_faculty': uni['notable_faculty'],
                    'program_strengths': uni['program_strengths'],
                    'application_deadline': uni['application_deadline'],
                    'description': f"A {uni['type'].lower()} university in {uni['country_name']}",
                    # Additional fields for frontend compatibility
                    'program_name': program_name,
                    'programName': program_name,  # Frontend expects this field
                    'duration': "2-4 years",  # Default duration
                    'requirements': requirements,
                    'faculty_highlights': faculty_highlights,
                    'facultyHighlights': faculty_highlights,  # Frontend expects this field
                    'campus_life': f"Campus life at {uni['name']} offers a vibrant community with diverse activities and modern facilities.",
                    'campusLife': f"Campus life at {uni['name']} offers a vibrant community with diverse activities and modern facilities.",  # Frontend expects this field
                    'strengths': strengths,
                    'match_score': 0  # Default match score, will be updated by recommendation engine
                }
                formatted_universities.append(formatted_uni)
            
            return formatted_universities
            
        except mysql.connector.Error as err:
            print(f"Error fetching universities: {err}")
            return self._get_minimal_fallback_data()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def get_university_by_id(self, university_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific university by ID
        """
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT * FROM universities WHERE id = %s
            """
            cursor.execute(query, (university_id,))
            uni = cursor.fetchone()
            
            if uni:
                return {
                    'id': uni['id'],
                    'name': uni['name'],
                    'country': uni['country_name'],
                    'country_code': uni['country_code'],
                    'website': uni['website'],
                    'ranking': uni['global_ranking'],
                    'tuition_fee': uni['tuition_fee_usd'],
                    'scholarship_available': bool(uni['scholarship_available']),
                    'admission_rate': uni['admission_rate'],
                    'student_population': uni['student_population'],
                    'founded_year': uni['founded_year'],
                    'type': uni['type'],
                    'research_areas': uni['research_areas'].split(', ') if uni['research_areas'] else [],
                    'campus_size': uni['campus_size'],
                    'admission_requirements': uni['admission_requirements'],
                    'notable_faculty': uni['notable_faculty'],
                    'program_strengths': uni['program_strengths'],
                    'application_deadline': uni['application_deadline'],
                    'description': f"A {uni['type'].lower()} university in {uni['country_name']}"
                }
            return None
            
        except mysql.connector.Error as err:
            print(f"Error fetching university by ID: {err}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def search_universities(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search universities by name, country, or research areas
        """
        conn = self.get_connection()
        if not conn:
            return self._get_minimal_fallback_data()[:limit]
        
        try:
            cursor = conn.cursor(dictionary=True)
            search_query = """
            SELECT id, country_code, country_name, name, website, global_ranking,
                   tuition_fee_usd, scholarship_available, admission_rate,
                   student_population, founded_year, type, research_areas, campus_size,
                   admission_requirements, notable_faculty, program_strengths, application_deadline
            FROM universities 
            WHERE name LIKE %s 
               OR country_name LIKE %s 
               OR research_areas LIKE %s
            ORDER BY 
                CASE WHEN name LIKE %s THEN 1
                     WHEN country_name LIKE %s THEN 2
                     ELSE 3 END,
                COALESCE(global_ranking, 9999),
                name
            LIMIT %s
            """
            
            search_term = f"%{query}%"
            exact_term = f"{query}%"
            cursor.execute(search_query, (search_term, search_term, search_term, exact_term, exact_term, limit))
            universities = cursor.fetchall()
            
            formatted_universities = []
            for uni in universities:
                formatted_uni = {
                    'id': uni['id'],
                    'name': uni['name'],
                    'country': uni['country_name'],
                    'country_code': uni['country_code'],
                    'website': uni['website'],
                    'ranking': uni['global_ranking'],
                    'tuition_fee': uni['tuition_fee_usd'],
                    'scholarship_available': bool(uni['scholarship_available']),
                    'admission_rate': uni['admission_rate'],
                    'student_population': uni['student_population'],
                    'founded_year': uni['founded_year'],
                    'type': uni['type'],
                    'research_areas': uni['research_areas'].split(', ') if uni['research_areas'] else [],
                    'campus_size': uni['campus_size'],
                    'admission_requirements': uni['admission_requirements'],
                    'notable_faculty': uni['notable_faculty'],
                    'program_strengths': uni['program_strengths'],
                    'application_deadline': uni['application_deadline'],
                    'description': f"A {uni['type'].lower()} university in {uni['country_name']}"
                }
                formatted_universities.append(formatted_uni)
            
            return formatted_universities
            
        except mysql.connector.Error as err:
            print(f"Error searching universities: {err}")
            return self._get_minimal_fallback_data()[:limit]
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def filter_universities(self, filters: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        """
        Filter universities based on various criteria
        """
        conn = self.get_connection()
        if not conn:
            return self._get_minimal_fallback_data()[:limit]
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Build dynamic query based on filters
            where_conditions = []
            params = []
            
            if 'country' in filters and filters['country']:
                where_conditions.append("country_name = %s")
                params.append(filters['country'])
            
            if 'max_tuition' in filters and filters['max_tuition']:
                where_conditions.append("(tuition_fee_usd IS NULL OR tuition_fee_usd <= %s)")
                params.append(filters['max_tuition'])
            
            if 'min_ranking' in filters and filters['min_ranking']:
                where_conditions.append("(global_ranking IS NULL OR global_ranking >= %s)")
                params.append(filters['min_ranking'])
            
            if 'max_ranking' in filters and filters['max_ranking']:
                where_conditions.append("(global_ranking IS NULL OR global_ranking <= %s)")
                params.append(filters['max_ranking'])
            
            if 'scholarship_available' in filters:
                where_conditions.append("scholarship_available = %s")
                params.append(filters['scholarship_available'])
            
            if 'university_type' in filters and filters['university_type']:
                where_conditions.append("type = %s")
                params.append(filters['university_type'])
            
            if 'research_area' in filters and filters['research_area']:
                where_conditions.append("research_areas LIKE %s")
                params.append(f"%{filters['research_area']}%")
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            query = f"""
            SELECT id, country_code, country_name, name, website, global_ranking,
                   tuition_fee_usd, scholarship_available, admission_rate,
                   student_population, founded_year, type, research_areas, campus_size,
                   admission_requirements, notable_faculty, program_strengths, application_deadline
            FROM universities 
            WHERE {where_clause}
            ORDER BY COALESCE(global_ranking, 9999), name
            LIMIT %s
            """
            
            params.append(limit)
            cursor.execute(query, params)
            universities = cursor.fetchall()
            
            formatted_universities = []
            for uni in universities:
                formatted_uni = {
                    'id': uni['id'],
                    'name': uni['name'],
                    'country': uni['country_name'],
                    'country_code': uni['country_code'],
                    'website': uni['website'],
                    'ranking': uni['global_ranking'],
                    'tuition_fee': uni['tuition_fee_usd'],
                    'scholarship_available': bool(uni['scholarship_available']),
                    'admission_rate': uni['admission_rate'],
                    'student_population': uni['student_population'],
                    'founded_year': uni['founded_year'],
                    'type': uni['type'],
                    'research_areas': uni['research_areas'].split(', ') if uni['research_areas'] else [],
                    'campus_size': uni['campus_size'],
                    'admission_requirements': uni['admission_requirements'],
                    'notable_faculty': uni['notable_faculty'],
                    'program_strengths': uni['program_strengths'],
                    'application_deadline': uni['application_deadline'],
                    'description': f"A {uni['type'].lower()} university in {uni['country_name']}"
                }
                formatted_universities.append(formatted_uni)
            
            return formatted_universities
            
        except mysql.connector.Error as err:
            print(f"Error filtering universities: {err}")
            return self._get_minimal_fallback_data()[:limit]
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def add_university(self, university_data: Dict[str, Any]) -> bool:
        """
        Add a new university to the database
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO universities (
                country_code, country_name, name, website, global_ranking,
                tuition_fee_usd, scholarship_available, admission_rate,
                student_population, founded_year, type, research_areas, campus_size
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            research_areas_str = ', '.join(university_data.get('research_areas', []))
            
            cursor.execute(insert_query, (
                university_data.get('country_code', ''),
                university_data.get('country', ''),
                university_data.get('name', ''),
                university_data.get('website', ''),
                university_data.get('ranking'),
                university_data.get('tuition_fee'),
                university_data.get('scholarship_available', False),
                university_data.get('admission_rate'),
                university_data.get('student_population'),
                university_data.get('founded_year'),
                university_data.get('type', 'Public'),
                research_areas_str,
                university_data.get('campus_size', 'Medium')
            ))
            
            conn.commit()
            return True
            
        except mysql.connector.Error as err:
            print(f"Error adding university: {err}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def update_university(self, university_id: int, university_data: Dict[str, Any]) -> bool:
        """
        Update an existing university
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            params = []
            
            field_mapping = {
                'name': 'name',
                'country': 'country_name',
                'country_code': 'country_code',
                'website': 'website',
                'ranking': 'global_ranking',
                'tuition_fee': 'tuition_fee_usd',
                'scholarship_available': 'scholarship_available',
                'admission_rate': 'admission_rate',
                'student_population': 'student_population',
                'founded_year': 'founded_year',
                'type': 'type',
                'campus_size': 'campus_size'
            }
            
            for key, db_field in field_mapping.items():
                if key in university_data:
                    update_fields.append(f"{db_field} = %s")
                    params.append(university_data[key])
            
            if 'research_areas' in university_data:
                update_fields.append("research_areas = %s")
                params.append(', '.join(university_data['research_areas']))
            
            if not update_fields:
                return False
            
            params.append(university_id)
            
            update_query = f"""
            UPDATE universities 
            SET {', '.join(update_fields)}
            WHERE id = %s
            """
            
            cursor.execute(update_query, params)
            conn.commit()
            
            return cursor.rowcount > 0
            
        except mysql.connector.Error as err:
            print(f"Error updating university: {err}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def delete_university(self, university_id: int) -> bool:
        """
        Delete a university from the database
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            delete_query = "DELETE FROM universities WHERE id = %s"
            cursor.execute(delete_query, (university_id,))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except mysql.connector.Error as err:
            print(f"Error deleting university: {err}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        """
        conn = self.get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Total universities
            cursor.execute("SELECT COUNT(*) as total FROM universities")
            total = cursor.fetchone()['total']
            
            # Universities by country
            cursor.execute("""
                SELECT country_name, COUNT(*) as count 
                FROM universities 
                GROUP BY country_name 
                ORDER BY count DESC 
                LIMIT 10
            """)
            by_country = cursor.fetchall()
            
            # Average tuition by country
            cursor.execute("""
                SELECT country_name, AVG(tuition_fee_usd) as avg_tuition 
                FROM universities 
                WHERE tuition_fee_usd IS NOT NULL
                GROUP BY country_name 
                HAVING COUNT(*) >= 5
                ORDER BY avg_tuition ASC 
                LIMIT 10
            """)
            avg_tuition = cursor.fetchall()
            
            return {
                'total_universities': total,
                'universities_by_country': by_country,
                'average_tuition_by_country': avg_tuition
            }
            
        except mysql.connector.Error as err:
            print(f"Error getting statistics: {err}")
            return {}
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    async def generate_universities_for_field(self, field: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate universities for a specific field using GPT
        """
        try:
            # Get some real universities as base
            real_universities = self.search_universities(field, limit=3)
            
            if real_universities:
                # Use GPT to enhance the first university
                enhanced = await self.gpt_enhancer.generate_university_data(
                    real_universities[0]['name'],
                    real_universities[0]['country'],
                    field
                )
                if enhanced:
                    real_universities[0].update(enhanced)
                
                return real_universities[:count]
            else:
                # Generate completely new universities
                generated_universities = []
                for i in range(count):
                    generated = await self.gpt_enhancer.generate_university_data(
                        f"University of {field} Excellence {i+1}",
                        "United States",
                        field
                    )
                    if generated:
                        generated_universities.append(generated)
                
                return generated_universities
                
        except Exception as e:
            print(f"Error generating universities for field: {e}")
            return self._get_minimal_fallback_data()[:count]
    
    async def generate_university_with_gpt(self, university_name: str, country: str, field: str = "Computer Science") -> Optional[Dict[str, Any]]:
        """
        Generate detailed university data using GPT
        """
        try:
            return await self.gpt_enhancer.generate_university_data(university_name, country, field)
        except Exception as e:
            print(f"Error generating university with GPT: {e}")
            return None
    
    async def get_all_countries(self) -> List[Dict[str, str]]:
        """
        Get all unique countries from the database, consolidating duplicates
        """
        conn = self.get_connection()
        if not conn:
            return [
                {'code': 'US', 'name': 'United States'},
                {'code': 'UK', 'name': 'United Kingdom'},
                {'code': 'CA', 'name': 'Canada'},
                {'code': 'AU', 'name': 'Australia'},
                {'code': 'DE', 'name': 'Germany'}
            ]
        
        # Country consolidation mapping
        country_consolidation = {
            'Hong Kong SAR': 'Hong Kong',
            'China (Mainland)': 'China',
            'Macau SAR': 'Macau'
        }
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT DISTINCT country_code as code, country_name as name 
            FROM universities 
            WHERE country_code IS NOT NULL 
              AND country_code != 'Unknown' 
              AND country_code != 'XX'
              AND country_name IS NOT NULL 
              AND country_name != 'Unknown'
              AND country_name != country_code
              AND LENGTH(country_code) = 2
              AND country_code REGEXP '^[A-Z]{2}$'
            ORDER BY country_name
            """
            cursor.execute(query)
            raw_countries = cursor.fetchall()
            
            # Consolidate duplicates
            consolidated = {}
            for country in raw_countries:
                name = country['name']
                code = country['code']
                
                # Apply consolidation mapping
                if name in country_consolidation:
                    name = country_consolidation[name]
                
                # Use the first code encountered for each consolidated name
                if name not in consolidated:
                    consolidated[name] = code
            
            # Convert back to list format
            countries = [{'code': code, 'name': name} for name, code in consolidated.items()]
            countries.sort(key=lambda x: x['name'])
            
            return countries
        except mysql.connector.Error as err:
            print(f"Error fetching countries: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    async def get_all_fields(self) -> List[str]:
        """
        Get all unique fields of study from the database, grouped by base name
        """
        conn = self.get_connection()
        if not conn:
            return [
                'Computer Science',
                'Engineering',
                'Business',
                'Medicine',
                'Physics',
                'Mathematics',
                'Biology',
                'Chemistry',
                'Economics',
                'Psychology'
            ]
        
        try:
            cursor = conn.cursor()
            query = """
            SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(research_areas, ',', numbers.n), ',', -1)) as field
            FROM universities
            CROSS JOIN (
                SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
                UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
            ) numbers
            WHERE research_areas IS NOT NULL 
            AND CHAR_LENGTH(research_areas) - CHAR_LENGTH(REPLACE(research_areas, ',', '')) >= numbers.n - 1
            AND TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(research_areas, ',', numbers.n), ',', -1)) != ''
            ORDER BY field
            """
            cursor.execute(query)
            raw_fields = [row[0] for row in cursor.fetchall()]
            
            # Group fields by base name (remove ranking numbers and suffixes)
            grouped_fields = set()
            for field in raw_fields:
                # Remove common ranking patterns and suffixes
                clean_field = field
                # Remove patterns like "1001+", "101 12", "201 250th", "301 400th", etc.
                import re
                clean_field = re.sub(r'\s*\d+\s*\+?$', '', clean_field)  # Remove trailing numbers with optional +
                clean_field = re.sub(r'\s*\d+\s+\d+\w*$', '', clean_field)  # Remove patterns like "101 12", "201 250th"
                clean_field = re.sub(r'\s*\d+\w*$', '', clean_field)  # Remove trailing numbers with ordinal suffixes
                clean_field = clean_field.strip()
                
                if clean_field and len(clean_field) > 2:  # Only include meaningful field names
                    grouped_fields.add(clean_field)
            
            return sorted(list(grouped_fields))
        except mysql.connector.Error as err:
            print(f"Error fetching fields: {err}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def _get_minimal_fallback_data(self) -> List[Dict[str, Any]]:
        """
        Minimal fallback data when database is not available
        """
        return [
            {
                'id': 1,
                'name': 'Massachusetts Institute of Technology',
                'country': 'United States',
                'country_code': 'US',
                'website': 'https://www.mit.edu',
                'ranking': 1,
                'tuition_fee': 57986,
                'scholarship_available': True,
                'admission_rate': 6.7,
                'student_population': 11934,
                'founded_year': 1861,
                'type': 'Private',
                'research_areas': ['Computer Science', 'Engineering', 'Physics', 'Mathematics'],
                'campus_size': 'Large',
                'description': 'A private research university in Cambridge, Massachusetts'
            },
            {
                'id': 2,
                'name': 'Stanford University',
                'country': 'United States',
                'country_code': 'US',
                'website': 'https://www.stanford.edu',
                'ranking': 2,
                'tuition_fee': 56169,
                'scholarship_available': True,
                'admission_rate': 4.3,
                'student_population': 17249,
                'founded_year': 1885,
                'type': 'Private',
                'research_areas': ['Computer Science', 'Engineering', 'Business', 'Medicine'],
                'campus_size': 'Very Large',
                'description': 'A private research university in Stanford, California'
            }
        ]

# Create a global instance
university_db = UniversityDatabaseMySQL()