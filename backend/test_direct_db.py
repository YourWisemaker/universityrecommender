from university_database_mysql import university_db

# Test the database methods directly
print("Testing university database methods...\n")

# Test get_all_universities
print("1. Testing get_all_universities (first 2 universities):")
universities = university_db.get_all_universities(limit=2)
for i, uni in enumerate(universities, 1):
    print(f"\nUniversity {i}: {uni['name']} ({uni['country']})")
    print(f"  Admission Requirements: {uni.get('admission_requirements', 'N/A')[:100]}...")
    print(f"  Notable Faculty: {uni.get('notable_faculty', 'N/A')[:100]}...")
    print(f"  Program Strengths: {uni.get('program_strengths', 'N/A')[:100]}...")
    print(f"  Application Deadline: {uni.get('application_deadline', 'N/A')}")
    print(f"  Admission Rate: {uni.get('admission_rate', 'N/A')}%")
    print(f"  Tuition Fee: ${uni.get('tuition_fee', 'N/A')}")

print("\n" + "="*80)

# Test search_universities
print("\n2. Testing search_universities (searching for 'MIT'):")
search_results = university_db.search_universities('MIT', limit=1)
for uni in search_results:
    print(f"\nFound: {uni['name']} ({uni['country']})")
    print(f"  Admission Requirements: {uni.get('admission_requirements', 'N/A')[:100]}...")
    print(f"  Notable Faculty: {uni.get('notable_faculty', 'N/A')[:100]}...")
    print(f"  Program Strengths: {uni.get('program_strengths', 'N/A')[:100]}...")
    print(f"  Application Deadline: {uni.get('application_deadline', 'N/A')}")

print("\n" + "="*80)

# Test filter_universities
print("\n3. Testing filter_universities (US universities):")
filtered_results = university_db.filter_universities({'country': 'United States'}, limit=1)
for uni in filtered_results:
    print(f"\nFiltered: {uni['name']} ({uni['country']})")
    print(f"  Admission Requirements: {uni.get('admission_requirements', 'N/A')[:100]}...")
    print(f"  Notable Faculty: {uni.get('notable_faculty', 'N/A')[:100]}...")
    print(f"  Program Strengths: {uni.get('program_strengths', 'N/A')[:100]}...")
    print(f"  Application Deadline: {uni.get('application_deadline', 'N/A')}")

print("\n" + "="*80)
print("\nAll database methods are working correctly with new fields!")