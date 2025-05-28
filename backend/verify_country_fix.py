#!/usr/bin/env python3

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_country_data():
    """Verify the country data in the database"""
    
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'university_recommender')
        )
        
        cursor = connection.cursor()
        
        # Check total universities
        cursor.execute("SELECT COUNT(*) FROM universities")
        total_count = cursor.fetchone()[0]
        print(f"Total universities in database: {total_count}")
        
        # Check if we have research_areas data (this is what we updated)
        cursor.execute("SELECT COUNT(*) FROM universities WHERE research_areas IS NOT NULL AND research_areas != ''")
        research_areas_count = cursor.fetchone()[0]
        print(f"Universities with research areas data: {research_areas_count}")
        
        # Show some examples of updated universities
        print("\nExamples of universities with research areas:")
        cursor.execute("""
            SELECT name, LEFT(research_areas, 100) as research_areas_preview, global_ranking 
            FROM universities 
            WHERE research_areas IS NOT NULL AND research_areas != ''
            AND global_ranking IS NOT NULL
            ORDER BY global_ranking ASC 
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        for name, research_areas, ranking in results:
            print(f"  {ranking:3d}. {name[:40]:<40} | {research_areas}...")
        
        # Check for California Institute of Technology specifically
        print("\nChecking California Institute of Technology:")
        cursor.execute("""
            SELECT name, research_areas, global_ranking
            FROM universities 
            WHERE name LIKE '%California Institute%' OR name LIKE '%Caltech%'
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        for name, research_areas, ranking in results:
            research_preview = research_areas[:100] + '...' if research_areas and len(research_areas) > 100 else research_areas
            print(f"  {name} (Rank: {ranking}) | Research: {research_preview}")
        
        # Show top universities by ranking
        print("\nTop 10 universities by ranking:")
        cursor.execute("""
            SELECT name, global_ranking, LEFT(research_areas, 60) as research_preview
            FROM universities 
            WHERE global_ranking IS NOT NULL AND global_ranking > 0
            ORDER BY global_ranking ASC 
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        for name, ranking, research_areas in results:
            research_preview = research_areas if research_areas else 'No research areas'
            print(f"  {ranking:3d}. {name[:40]:<40} | {research_preview}")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    verify_country_data()

if __name__ == "__main__":
    main()