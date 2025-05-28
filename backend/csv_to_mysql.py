import csv
import mysql.connector
import random
import asyncio
import os
from dotenv import load_dotenv
from gpt_university_enhancer import GPTUniversityEnhancer
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

class CSVToMySQLConverter:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'universitydb')
        }
        self.enhancer = GPTUniversityEnhancer()
        
    def create_database_and_table(self):
        """Create database and universities table"""
        try:
            # Connect without database first
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                port=self.db_config['port']
            )
            cursor = conn.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            cursor.execute(f"USE {self.db_config['database']}")
            
            # Create universities table with enhanced fields
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS universities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                country_code VARCHAR(2) NOT NULL,
                country_name VARCHAR(100) NOT NULL,
                name VARCHAR(255) NOT NULL,
                website VARCHAR(500),
                global_ranking INT DEFAULT NULL,
                tuition_fee_usd DECIMAL(10,2) DEFAULT NULL,
                tuition_fee_local DECIMAL(10,2) DEFAULT NULL,
                local_currency VARCHAR(3) DEFAULT NULL,
                scholarship_available BOOLEAN DEFAULT FALSE,
                admission_rate DECIMAL(5,2) DEFAULT NULL,
                student_population INT DEFAULT NULL,
                founded_year INT DEFAULT NULL,
                type ENUM('Public', 'Private', 'Non-profit', 'For-profit') DEFAULT 'Public',
                research_areas TEXT,
                strengths TEXT,
                description TEXT,
                campus_size VARCHAR(50),
                location_city VARCHAR(100),
                location_state VARCHAR(100),
                admission_requirements TEXT,
                notable_faculty TEXT,
                program_strengths TEXT,
                application_deadline VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_country (country_code),
                INDEX idx_ranking (global_ranking),
                INDEX idx_tuition (tuition_fee_usd),
                INDEX idx_name (name)
            )
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            print("Database and table created successfully!")
            
        except mysql.connector.Error as err:
            print(f"Error creating database/table: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def get_country_name(self, country_code: str) -> str:
        """Convert country code to country name"""
        country_mapping = {
            'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AL': 'Albania',
            'AM': 'Armenia', 'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria',
            'AU': 'Australia', 'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina',
            'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria',
            'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 'BN': 'Brunei',
            'BO': 'Bolivia', 'BR': 'Brazil', 'BS': 'Bahamas', 'BT': 'Bhutan',
            'BW': 'Botswana', 'BY': 'Belarus', 'BZ': 'Belize', 'CA': 'Canada',
            'CD': 'Democratic Republic of the Congo', 'CF': 'Central African Republic',
            'CG': 'Republic of the Congo', 'CH': 'Switzerland', 'CI': 'Ivory Coast',
            'CL': 'Chile', 'CM': 'Cameroon', 'CN': 'China', 'CO': 'Colombia',
            'CR': 'Costa Rica', 'CU': 'Cuba', 'CV': 'Cape Verde', 'CY': 'Cyprus',
            'CZ': 'Czech Republic', 'DE': 'Germany', 'DJ': 'Djibouti', 'DK': 'Denmark',
            'DM': 'Dominica', 'DO': 'Dominican Republic', 'DZ': 'Algeria', 'EC': 'Ecuador',
            'EE': 'Estonia', 'EG': 'Egypt', 'ER': 'Eritrea', 'ES': 'Spain',
            'ET': 'Ethiopia', 'FI': 'Finland', 'FJ': 'Fiji', 'FM': 'Micronesia',
            'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom', 'GD': 'Grenada',
            'GE': 'Georgia', 'GH': 'Ghana', 'GM': 'Gambia', 'GN': 'Guinea',
            'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'GT': 'Guatemala', 'GW': 'Guinea-Bissau',
            'GY': 'Guyana', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HR': 'Croatia',
            'HT': 'Haiti', 'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland',
            'IL': 'Israel', 'IN': 'India', 'IQ': 'Iraq', 'IR': 'Iran',
            'IS': 'Iceland', 'IT': 'Italy', 'JM': 'Jamaica', 'JO': 'Jordan',
            'JP': 'Japan', 'KE': 'Kenya', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia',
            'KI': 'Kiribati', 'KM': 'Comoros', 'KN': 'Saint Kitts and Nevis',
            'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan',
            'LA': 'Laos', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LI': 'Liechtenstein',
            'LK': 'Sri Lanka', 'LR': 'Liberia', 'LS': 'Lesotho', 'LT': 'Lithuania',
            'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco',
            'MC': 'Monaco', 'MD': 'Moldova', 'ME': 'Montenegro', 'MG': 'Madagascar',
            'MH': 'Marshall Islands', 'MK': 'North Macedonia', 'ML': 'Mali', 'MM': 'Myanmar',
            'MN': 'Mongolia', 'MO': 'Macau', 'MR': 'Mauritania', 'MT': 'Malta',
            'MU': 'Mauritius', 'MV': 'Maldives', 'MW': 'Malawi', 'MX': 'Mexico',
            'MY': 'Malaysia', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger',
            'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway',
            'NP': 'Nepal', 'NR': 'Nauru', 'NZ': 'New Zealand', 'OM': 'Oman',
            'PA': 'Panama', 'PE': 'Peru', 'PG': 'Papua New Guinea', 'PH': 'Philippines',
            'PK': 'Pakistan', 'PL': 'Poland', 'PT': 'Portugal', 'PW': 'Palau',
            'PY': 'Paraguay', 'QA': 'Qatar', 'RO': 'Romania', 'RS': 'Serbia',
            'RU': 'Russia', 'RW': 'Rwanda', 'SA': 'Saudi Arabia', 'SB': 'Solomon Islands',
            'SC': 'Seychelles', 'SD': 'Sudan', 'SE': 'Sweden', 'SG': 'Singapore',
            'SH': 'Saint Helena', 'SI': 'Slovenia', 'SK': 'Slovakia', 'SL': 'Sierra Leone',
            'SM': 'San Marino', 'SN': 'Senegal', 'SO': 'Somalia', 'SR': 'Suriname',
            'SS': 'South Sudan', 'ST': 'Sao Tome and Principe', 'SV': 'El Salvador',
            'SY': 'Syria', 'SZ': 'Eswatini', 'TD': 'Chad', 'TG': 'Togo',
            'TH': 'Thailand', 'TJ': 'Tajikistan', 'TL': 'East Timor', 'TM': 'Turkmenistan',
            'TN': 'Tunisia', 'TO': 'Tonga', 'TR': 'Turkey', 'TT': 'Trinidad and Tobago',
            'TV': 'Tuvalu', 'TW': 'Taiwan', 'TZ': 'Tanzania', 'UA': 'Ukraine',
            'UG': 'Uganda', 'US': 'United States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan',
            'VA': 'Vatican City', 'VC': 'Saint Vincent and the Grenadines', 'VE': 'Venezuela',
            'VN': 'Vietnam', 'VU': 'Vanuatu', 'WS': 'Samoa', 'YE': 'Yemen',
            'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'
        }
        return country_mapping.get(country_code, country_code)
    
    def generate_enhanced_data(self, university_name: str, country_name: str) -> Dict[str, Any]:
        """Generate enhanced data for universities"""
        # Generate realistic data based on country and university type
        enhanced_data = {
            'global_ranking': random.randint(50, 2000) if random.random() > 0.3 else None,
            'tuition_fee_usd': round(random.uniform(5000, 60000), 2) if random.random() > 0.2 else None,
            'scholarship_available': random.choice([True, False]),
            'admission_rate': round(random.uniform(10, 90), 2) if random.random() > 0.3 else None,
            'student_population': random.randint(1000, 50000) if random.random() > 0.4 else None,
            'founded_year': random.randint(1800, 2020) if random.random() > 0.3 else None,
            'type': random.choice(['Public', 'Private', 'Non-profit']),
            'research_areas': ', '.join(random.sample([
                'Computer Science', 'Engineering', 'Medicine', 'Business', 'Law',
                'Arts', 'Sciences', 'Education', 'Psychology', 'Economics',
                'Biology', 'Chemistry', 'Physics', 'Mathematics', 'Literature'
            ], k=random.randint(2, 5))),
            'campus_size': random.choice(['Small', 'Medium', 'Large', 'Very Large']),
            'admission_requirements': self._generate_admission_requirements(country_name),
            'notable_faculty': self._generate_notable_faculty(),
            'program_strengths': self._generate_program_strengths(),
            'application_deadline': self._generate_application_deadline(country_name)
        }
        
        # Adjust tuition based on country
        if country_name in ['Germany', 'Norway', 'Finland', 'Denmark', 'Sweden']:
            enhanced_data['tuition_fee_usd'] = round(random.uniform(0, 2000), 2)  # Low/free tuition
        elif country_name in ['United States', 'United Kingdom', 'Australia', 'Canada']:
            enhanced_data['tuition_fee_usd'] = round(random.uniform(15000, 60000), 2)  # Higher tuition
        
        return enhanced_data
    
    def _generate_admission_requirements(self, country_name: str) -> str:
        """Generate realistic admission requirements"""
        base_requirements = [
            "High school diploma or equivalent",
            "Minimum GPA requirement",
            "English proficiency test (TOEFL/IELTS)",
            "Letters of recommendation",
            "Personal statement or essay"
        ]
        
        if country_name == "United States":
            base_requirements.extend(["SAT or ACT scores", "Extracurricular activities"])
        elif country_name == "United Kingdom":
            base_requirements.extend(["A-Level or equivalent qualifications", "UCAS application"])
        elif country_name in ["Germany", "Netherlands", "France"]:
            base_requirements.extend(["EU/International qualifications", "Language proficiency in local language"])
        
        return "; ".join(random.sample(base_requirements, k=random.randint(3, len(base_requirements))))
    
    def _generate_notable_faculty(self) -> str:
        """Generate notable faculty information with diverse and realistic names"""
        faculty_titles = ["Professor", "Dr.", "Prof.", "Associate Professor", "Assistant Professor"]
        
        # More diverse and realistic names
        first_names = [
            "Alexander", "Benjamin", "Catherine", "Daniel", "Elizabeth", "Francesco", "Gabriela", "Hassan", "Isabella", "Jonathan",
            "Katherine", "Leonardo", "Margaret", "Nicholas", "Olivia", "Patricia", "Quentin", "Rebecca", "Sebastian", "Theresa",
            "Ulrich", "Victoria", "William", "Xiaowei", "Yasmin", "Zachary", "Amelia", "Bruno", "Chloe", "Diego",
            "Elena", "Felix", "Grace", "Hugo", "Iris", "Julian", "Kimberly", "Lucas", "Maya", "Nathan",
            "Oscar", "Penelope", "Rafael", "Sophia", "Thomas", "Uma", "Vincent", "Wendy", "Xavier", "Zoe"
        ]
        
        last_names = [
            "Anderson", "Baker", "Chen", "Dubois", "Evans", "Fischer", "González", "Hansen", "Ibrahim", "Jackson",
            "Kumar", "López", "Müller", "Nielsen", "O'Connor", "Patel", "Quinn", "Rossi", "Schmidt", "Taylor",
            "Ueda", "Volkov", "Wang", "Yamamoto", "Zhang", "Andersson", "Bianchi", "Caron", "Delacroix", "Eriksson",
            "Fernández", "Gómez", "Hernández", "Ivanov", "Johansson", "Kowalski", "Larsson", "Moreau", "Nakamura", "Olsen",
            "Petrov", "Qian", "Ramos", "Singh", "Tanaka", "Uzun", "Varga", "Wilson", "Xu", "Zhu"
        ]
        
        specializations = [
            "Artificial Intelligence", "Biomedical Engineering", "Climate Science", "Data Science", "Environmental Studies",
            "Financial Economics", "Genetic Research", "Human-Computer Interaction", "International Relations", "Journalism",
            "Kinesiology", "Linguistics", "Materials Science", "Neuroscience", "Organic Chemistry",
            "Political Science", "Quantum Physics", "Renewable Energy", "Social Psychology", "Theoretical Mathematics",
            "Urban Planning", "Veterinary Medicine", "Women's Studies", "Xenobiology", "Youth Development", "Zoology",
            "Aerospace Engineering", "Biochemistry", "Cognitive Science", "Digital Media", "Educational Psychology",
            "Film Studies", "Global Health", "History", "Industrial Design", "Jazz Studies"
        ]
        
        # Generate achievements and recognitions
        achievements = [
            "Nobel Prize recipient", "Pulitzer Prize winner", "MacArthur Fellow", "Royal Society Fellow",
            "National Academy member", "Guggenheim Fellow", "Fulbright Scholar", "IEEE Fellow",
            "Distinguished Professor", "Research Excellence Award winner", "International recognition",
            "Leading researcher", "Published author", "Industry pioneer", "Innovation leader"
        ]
        
        faculty_list = []
        used_names = set()  # Prevent duplicate names
        
        for _ in range(random.randint(3, 5)):
            # Ensure unique names
            attempts = 0
            while attempts < 20:  # Prevent infinite loop
                title = random.choice(faculty_titles)
                first = random.choice(first_names)
                last = random.choice(last_names)
                full_name = f"{first} {last}"
                
                if full_name not in used_names:
                    used_names.add(full_name)
                    break
                attempts += 1
            
            spec = random.choice(specializations)
            
            # Sometimes add achievements
            if random.random() > 0.6:
                achievement = random.choice(achievements)
                faculty_entry = f"{title} {first} {last} ({spec}, {achievement})"
            else:
                faculty_entry = f"{title} {first} {last} ({spec})"
            
            faculty_list.append(faculty_entry)
        
        return "; ".join(faculty_list)
    
    def _generate_program_strengths(self) -> str:
        """Generate program strengths"""
        strengths = [
            "Research Excellence", "Industry Partnerships", "International Exchange Programs",
            "State-of-the-art Facilities", "Small Class Sizes", "Experienced Faculty",
            "Career Services", "Alumni Network", "Innovation Labs", "Internship Opportunities",
            "Interdisciplinary Programs", "Online Learning Options", "Scholarship Programs",
            "Student Support Services", "Campus Life", "Sports Programs"
        ]
        
        return "; ".join(random.sample(strengths, k=random.randint(3, 6)))
    
    def _generate_application_deadline(self, country_name: str) -> str:
        """Generate application deadlines based on country"""
        if country_name == "United States":
            return random.choice(["January 15", "February 1", "March 1", "Rolling Admissions"])
        elif country_name == "United Kingdom":
            return random.choice(["January 15 (UCAS)", "June 30 (UCAS)", "September 30 (UCAS)"])
        elif country_name in ["Germany", "Netherlands", "France"]:
            return random.choice(["March 15", "May 1", "July 15", "September 1"])
        elif country_name in ["Australia", "New Zealand"]:
            return random.choice(["October 31", "December 1", "January 31"])
        else:
            return random.choice(["March 1", "May 15", "July 1", "September 15", "Rolling Admissions"])
    
    def load_csv_to_mysql(self, csv_file_path: str, batch_size: int = 100):
        """Load CSV data to MySQL with enhancements"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM universities")
            
            insert_sql = """
            INSERT INTO universities (
                country_code, country_name, name, website, global_ranking,
                tuition_fee_usd, scholarship_available, admission_rate,
                student_population, founded_year, type, research_areas, campus_size,
                admission_requirements, notable_faculty, program_strengths, application_deadline
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            batch_data = []
            processed_count = 0
            
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                
                for row in csv_reader:
                    if len(row) >= 3:
                        country_code = row[0]
                        university_name = row[1]
                        website = row[2] if len(row) > 2 else None
                        
                        country_name = self.get_country_name(country_code)
                        enhanced_data = self.generate_enhanced_data(university_name, country_name)
                        
                        batch_data.append((
                            country_code,
                            country_name,
                            university_name,
                            website,
                            enhanced_data['global_ranking'],
                            enhanced_data['tuition_fee_usd'],
                            enhanced_data['scholarship_available'],
                            enhanced_data['admission_rate'],
                            enhanced_data['student_population'],
                            enhanced_data['founded_year'],
                            enhanced_data['type'],
                            enhanced_data['research_areas'],
                            enhanced_data['campus_size'],
                            enhanced_data['admission_requirements'],
                            enhanced_data['notable_faculty'],
                            enhanced_data['program_strengths'],
                            enhanced_data['application_deadline']
                        ))
                        
                        if len(batch_data) >= batch_size:
                            cursor.executemany(insert_sql, batch_data)
                            conn.commit()
                            processed_count += len(batch_data)
                            print(f"Processed {processed_count} universities...")
                            batch_data = []
                
                # Insert remaining data
                if batch_data:
                    cursor.executemany(insert_sql, batch_data)
                    conn.commit()
                    processed_count += len(batch_data)
            
            print(f"Successfully loaded {processed_count} universities to MySQL!")
            
        except mysql.connector.Error as err:
            print(f"Error loading data to MySQL: {err}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def create_indexes_and_views(self):
        """Create additional indexes and useful views"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Create useful views
            views_sql = [
                """
                CREATE OR REPLACE VIEW top_ranked_universities AS
                SELECT * FROM universities 
                WHERE global_ranking IS NOT NULL 
                ORDER BY global_ranking ASC
                LIMIT 100
                """,
                """
                CREATE OR REPLACE VIEW affordable_universities AS
                SELECT * FROM universities 
                WHERE tuition_fee_usd IS NOT NULL AND tuition_fee_usd < 10000
                ORDER BY tuition_fee_usd ASC
                """,
                """
                CREATE OR REPLACE VIEW universities_by_country AS
                SELECT country_name, COUNT(*) as university_count,
                       AVG(tuition_fee_usd) as avg_tuition,
                       AVG(global_ranking) as avg_ranking
                FROM universities 
                GROUP BY country_name
                ORDER BY university_count DESC
                """
            ]
            
            for view_sql in views_sql:
                cursor.execute(view_sql)
            
            conn.commit()
            print("Created indexes and views successfully!")
            
        except mysql.connector.Error as err:
            print(f"Error creating indexes/views: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def main():
    converter = CSVToMySQLConverter()
    
    print("Creating database and table...")
    converter.create_database_and_table()
    
    print("Loading CSV data to MySQL...")
    converter.load_csv_to_mysql('/Users/wisemaker/Sites/university-recommender/backend/world-universities.csv')
    
    print("Creating indexes and views...")
    converter.create_indexes_and_views()
    
    print("Conversion completed!")

if __name__ == "__main__":
    main()