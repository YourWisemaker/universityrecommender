import mysql.connector
from university_database_mysql import university_db

# Test database connection and check new fields
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='universitydb',
        port=3306
    )
    cursor = conn.cursor(dictionary=True)
    
    # Check if new fields exist and have data
    query = """
    SELECT name, country_name, admission_requirements, notable_faculty, 
           program_strengths, application_deadline, admission_rate, tuition_fee_usd
    FROM universities 
    LIMIT 3
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"Found {len(results)} universities in database")
    print("\n" + "="*80)
    
    for i, uni in enumerate(results, 1):
        print(f"\nUniversity {i}: {uni['name']} ({uni['country_name']})")
        print(f"Admission Requirements: {uni['admission_requirements'][:100] if uni['admission_requirements'] else 'N/A'}...")
        print(f"Notable Faculty: {uni['notable_faculty'][:100] if uni['notable_faculty'] else 'N/A'}...")
        print(f"Program Strengths: {uni['program_strengths'][:100] if uni['program_strengths'] else 'N/A'}...")
        print(f"Application Deadline: {uni['application_deadline'] if uni['application_deadline'] else 'N/A'}")
        print(f"Admission Rate: {uni['admission_rate']}%" if uni['admission_rate'] else "Admission Rate: N/A")
        print(f"Tuition Fee: ${uni['tuition_fee_usd']}" if uni['tuition_fee_usd'] else "Tuition Fee: N/A")
        print("-" * 80)
    
    # Check total count
    cursor.execute("SELECT COUNT(*) as total FROM universities")
    total = cursor.fetchone()
    print(f"\nTotal universities in database: {total['total']}")
    
    # Check how many have the new fields populated
    cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN admission_requirements IS NOT NULL AND admission_requirements != '' THEN 1 ELSE 0 END) as has_admission_req,
        SUM(CASE WHEN notable_faculty IS NOT NULL AND notable_faculty != '' THEN 1 ELSE 0 END) as has_faculty,
        SUM(CASE WHEN program_strengths IS NOT NULL AND program_strengths != '' THEN 1 ELSE 0 END) as has_strengths,
        SUM(CASE WHEN application_deadline IS NOT NULL AND application_deadline != '' THEN 1 ELSE 0 END) as has_deadline
    FROM universities
    """)
    
    stats = cursor.fetchone()
    print(f"\nField Population Statistics:")
    print(f"Total universities: {stats['total']}")
    print(f"Have admission requirements: {stats['has_admission_req']} ({stats['has_admission_req']/stats['total']*100:.1f}%)")
    print(f"Have notable faculty: {stats['has_faculty']} ({stats['has_faculty']/stats['total']*100:.1f}%)")
    print(f"Have program strengths: {stats['has_strengths']} ({stats['has_strengths']/stats['total']*100:.1f}%)")
    print(f"Have application deadline: {stats['has_deadline']} ({stats['has_deadline']/stats['total']*100:.1f}%)")
    
except mysql.connector.Error as err:
    print(f"Database error: {err}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")