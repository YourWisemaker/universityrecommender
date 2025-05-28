#!/usr/bin/env python3

import json
import mysql.connector
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional

# Load environment variables
load_dotenv()

class DatabaseUpdater:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'universitydb')
        }
    
    def get_connection(self):
        """Get MySQL database connection"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            return None
    
    def clean_subjects(self, subjects: List[str]) -> str:
        """Clean and format subjects list for research_areas column"""
        if not subjects:
            return ""
        
        # Remove ranking numbers and clean up subject names
        cleaned_subjects = []
        for subject in subjects:
            # Remove ranking patterns like "3rd", "1st", etc.
            cleaned = subject
            # Remove common ranking suffixes
            for suffix in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', 
                          '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th']:
                cleaned = cleaned.replace(suffix, '').strip()
            
            # Skip empty or very short entries
            if len(cleaned) > 2:
                cleaned_subjects.append(cleaned)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_subjects = []
        for subject in cleaned_subjects:
            if subject not in seen:
                seen.add(subject)
                unique_subjects.append(subject)
        
        return ", ".join(unique_subjects)
    
    def map_country_code(self, country_name: str) -> str:
        """Map country names to country codes"""
        country_mapping = {
            'United Kingdom': 'UK',
            'United States': 'US',
            'Canada': 'CA',
            'Australia': 'AU',
            'Germany': 'DE',
            'France': 'FR',
            'Netherlands': 'NL',
            'Switzerland': 'CH',
            'Sweden': 'SE',
            'Denmark': 'DK',
            'Norway': 'NO',
            'Finland': 'FI',
            'Belgium': 'BE',
            'Austria': 'AT',
            'Italy': 'IT',
            'Spain': 'ES',
            'Japan': 'JP',
            'South Korea': 'KR',
            'China': 'CN',
            'Hong Kong': 'HK',
            'Singapore': 'SG',
            'New Zealand': 'NZ',
            'Ireland': 'IE',
            'Israel': 'IL',
            'Brazil': 'BR',
            'Chile': 'CL',
            'Mexico': 'MX',
            'South Africa': 'ZA',
            'India': 'IN',
            'Thailand': 'TH',
            'Malaysia': 'MY',
            'Taiwan': 'TW',
            'Russia': 'RU',
            'Poland': 'PL',
            'Czech Republic': 'CZ',
            'Hungary': 'HU',
            'Portugal': 'PT',
            'Greece': 'GR',
            'Turkey': 'TR',
            'Estonia': 'EE',
            'Latvia': 'LV',
            'Lithuania': 'LT',
            'Slovenia': 'SI',
            'Croatia': 'HR',
            'Cyprus': 'CY',
            'Luxembourg': 'LU',
            'Iceland': 'IS',
            'Lebanon': 'LB',
            'United Arab Emirates': 'AE',
            'Qatar': 'QA',
            'Saudi Arabia': 'SA',
            'Egypt': 'EG',
            'Morocco': 'MA',
            'Tunisia': 'TN',
            'Jordan': 'JO',
            'Pakistan': 'PK',
            'Bangladesh': 'BD',
            'Sri Lanka': 'LK',
            'Philippines': 'PH',
            'Indonesia': 'ID',
            'Vietnam': 'VN',
            'Colombia': 'CO',
            'Argentina': 'AR',
            'Peru': 'PE',
            'Ecuador': 'EC',
            'Uruguay': 'UY',
            'Venezuela': 'VE',
            'Costa Rica': 'CR',
            'Panama': 'PA',
            'Jamaica': 'JM',
            'Trinidad and Tobago': 'TT',
            'Barbados': 'BB',
            'Ghana': 'GH',
            'Nigeria': 'NG',
            'Kenya': 'KE',
            'Uganda': 'UG',
            'Tanzania': 'TZ',
            'Ethiopia': 'ET',
            'Botswana': 'BW',
            'Zimbabwe': 'ZW',
            'Zambia': 'ZM',
            'Malawi': 'MW',
            'Mozambique': 'MZ'
        }
        return country_mapping.get(country_name, '')
    
    def parse_student_population(self, number_students: str) -> Optional[int]:
        """Parse student population from string"""
        if not number_students:
            return None
        try:
            # Remove commas and convert to int
            return int(number_students.replace(',', ''))
        except (ValueError, AttributeError):
            return None
    
    def parse_admission_rate(self, intl_students: str) -> Optional[float]:
        """Parse international students percentage as admission rate approximation"""
        if not intl_students:
            return None
        try:
            # Use international students percentage as a proxy for admission rate
            return float(intl_students)
        except (ValueError, AttributeError):
            return None
    
    def update_university(self, conn, university_data: Dict[str, Any]) -> str:
        """Update or insert a single university record"""
        # Map JSON fields to database columns first
        name = university_data.get('name', '')
        global_ranking = int(university_data.get('rank', 0)) if university_data.get('rank') else None
        website = university_data.get('web_address', '')
        country_name = university_data.get('country') or 'Unknown'
        country_code = university_data.get('country_code') or self.map_country_code(country_name)
        student_population = self.parse_student_population(university_data.get('number_students'))
        admission_rate = self.parse_admission_rate(university_data.get('intl_students'))
        research_areas = self.clean_subjects(university_data.get('subjects', []))
        description = university_data.get('description', '')
        
        # Skip if no name
        if not name:
            print("Skipping university with no name")
            return 'skip'
            
        try:
            cursor = conn.cursor()
            
            # Check if university exists
            check_query = "SELECT id FROM universities WHERE name = %s"
            cursor.execute(check_query, (name,))
            existing = cursor.fetchone()
            cursor.fetchall()  # Clear any remaining results
            
            if existing:
                # Update existing university
                update_query = """
                UPDATE universities SET 
                    global_ranking = %s,
                    website = %s,
                    country_name = %s,
                    country_code = %s,
                    student_population = %s,
                    admission_rate = %s,
                    research_areas = %s,
                    description = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE name = %s
                """
                cursor.execute(update_query, (
                    global_ranking, website, country_name, country_code,
                    student_population, admission_rate, research_areas, description, name
                ))
                cursor.fetchall()  # Clear any remaining results
                print(f"Updated: {name} (Rank: {global_ranking})")
                cursor.close()
                return 'updated'
            else:
                # Insert new university
                insert_query = """
                INSERT INTO universities (
                    name, global_ranking, website, country_name, country_code,
                    student_population, admission_rate, research_areas, description,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
                cursor.execute(insert_query, (
                    name, global_ranking, website, country_name, country_code,
                    student_population, admission_rate, research_areas, description
                ))
                cursor.fetchall()  # Clear any remaining results
                print(f"Inserted: {name} (Rank: {global_ranking})")
                cursor.close()
                return 'inserted'
            
        except mysql.connector.Error as err:
            print(f"Error updating {name}: {err}")
            return 'error'
    
    def update_database_from_json(self, json_file_path: str):
        """Update database from JSON file"""
        # Load JSON data
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                universities_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File {json_file_path} not found")
            return
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return
        
        print(f"Loaded {len(universities_data)} universities from JSON")
        
        # Connect to database
        conn = self.get_connection()
        if not conn:
            print("Failed to connect to database")
            return
        
        try:
            updated_count = 0
            inserted_count = 0
            
            for university in universities_data:
                result = self.update_university(conn, university)
                if result == 'updated':
                    updated_count += 1
                elif result == 'inserted':
                    inserted_count += 1
            
            # Commit all changes
            conn.commit()
            print(f"\nDatabase update completed:")
            print(f"- Updated: {updated_count} universities")
            print(f"- Inserted: {inserted_count} universities")
            print(f"- Total processed: {len(universities_data)} universities")
            
        except Exception as e:
            print(f"Error during database update: {e}")
            conn.rollback()
        finally:
            conn.close()

def main():
    json_file_path = "/Users/wisemaker/Sites/university-recommender/backend/updated_universities_fixed.json"
    
    updater = DatabaseUpdater()
    updater.update_database_from_json(json_file_path)

if __name__ == "__main__":
    main()