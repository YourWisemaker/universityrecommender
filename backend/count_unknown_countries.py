#!/usr/bin/env python3
import json

def count_unknown_countries():
    # Load the JSON data
    with open('updated_universities_fixed.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    total_universities = len(universities)
    unknown_count = 0
    known_count = 0
    null_count = 0
    
    unknown_examples = []
    
    for university in universities:
        country = university.get('country')
        if country == 'Unknown':
            unknown_count += 1
            if len(unknown_examples) < 10:
                unknown_examples.append({
                    'name': university.get('name', 'N/A'),
                    'web_address': university.get('web_address', 'N/A')
                })
        elif country in [None, '']:
            null_count += 1
        else:
            known_count += 1
    
    print(f"\n=== COUNTRY DATA ANALYSIS ===")
    print(f"Total universities: {total_universities}")
    print(f"Known countries: {known_count} ({known_count/total_universities*100:.1f}%)")
    print(f"Unknown countries: {unknown_count} ({unknown_count/total_universities*100:.1f}%)")
    print(f"Null/empty countries: {null_count} ({null_count/total_universities*100:.1f}%)")
    
    print(f"\n=== IMPROVEMENT SUMMARY ===")
    print(f"Successfully identified countries for {known_count} out of {total_universities} universities")
    print(f"Remaining universities with 'Unknown' country: {unknown_count}")
    
    if unknown_examples:
        print(f"\n=== EXAMPLES OF REMAINING UNKNOWN UNIVERSITIES ===")
        for i, uni in enumerate(unknown_examples, 1):
            print(f"{i}. {uni['name']}")
            print(f"   Web: {uni['web_address']}")
    
    # Calculate the percentage of successfully identified countries
    success_rate = (known_count / total_universities) * 100
    print(f"\n=== OVERALL SUCCESS RATE ===")
    print(f"Country identification success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("✅ Excellent! Most universities now have identified countries.")
    elif success_rate >= 60:
        print("✅ Good progress! Majority of universities have identified countries.")
    else:
        print("⚠️  More work needed to improve country identification.")

if __name__ == "__main__":
    count_unknown_countries()