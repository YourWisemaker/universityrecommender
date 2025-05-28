#!/usr/bin/env python3

import json

def check_country_status():
    """Check the final status of country data in the JSON file"""
    
    with open('/Users/wisemaker/Sites/university-recommender/backend/updated_universities_fixed.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    print(f"Total universities: {len(universities)}")
    
    # Count universities by country status
    unknown_count = 0
    known_count = 0
    null_count = 0
    
    country_counts = {}
    unknown_examples = []
    fixed_examples = []
    
    for uni in universities:
        country = uni.get('country')
        
        if country is None:
            null_count += 1
        elif country == 'Unknown':
            unknown_count += 1
            if len(unknown_examples) < 10:
                unknown_examples.append({
                    'name': uni.get('name', 'N/A'),
                    'web_address': uni.get('web_address', 'N/A')
                })
        else:
            known_count += 1
            country_counts[country] = country_counts.get(country, 0) + 1
            
            # Collect some examples of successfully identified countries
            if country in ['Indonesia', 'Philippines', 'Vietnam', 'Egypt', 'Turkey'] and len(fixed_examples) < 20:
                fixed_examples.append({
                    'name': uni.get('name', 'N/A'),
                    'country': country,
                    'country_code': uni.get('country_code', 'N/A')
                })
    
    print(f"\nCountry Status:")
    print(f"  Universities with known countries: {known_count}")
    print(f"  Universities with 'Unknown' country: {unknown_count}")
    print(f"  Universities with null country: {null_count}")
    
    print(f"\nTop 15 countries by university count:")
    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
    for country, count in sorted_countries[:15]:
        print(f"  {country:<20} | {count:4d} universities")
    
    print(f"\nExamples of successfully identified countries:")
    for example in fixed_examples:
        print(f"  {example['name'][:50]:<50} | {example['country']} ({example['country_code']})")
    
    print(f"\nExamples of universities still with 'Unknown' country:")
    for example in unknown_examples:
        print(f"  {example['name'][:50]:<50} | {example['web_address'][:60]}")
    
    # Check specific universities mentioned
    print(f"\nSpecific university checks:")
    for uni in universities:
        name = uni.get('name', '').lower()
        if 'gadjah mada' in name:
            print(f"  Gadjah Mada: {uni.get('name')} -> {uni.get('country')} ({uni.get('country_code')})")
        elif 'california institute' in name:
            print(f"  Caltech: {uni.get('name')} -> {uni.get('country')} ({uni.get('country_code')})")

def main():
    check_country_status()

if __name__ == "__main__":
    main()