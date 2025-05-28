#!/usr/bin/env python3
import json
import re
from collections import Counter

def analyze_unknown_countries():
    # Load the JSON data
    with open('updated_universities_fixed.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    unknown_universities = []
    
    # Find all universities with Unknown country
    for uni in universities:
        if uni.get('country') == 'Unknown':
            unknown_universities.append({
                'name': uni.get('name', ''),
                'web_address': uni.get('web_address', ''),
                'description': uni.get('description', '')[:100] + '...' if uni.get('description') else ''
            })
    
    print(f"Total universities with 'Unknown' country: {len(unknown_universities)}")
    print("\n" + "="*80)
    
    # Analyze patterns in university names
    print("\nAnalyzing university name patterns:")
    name_words = []
    for uni in unknown_universities:
        words = re.findall(r'\b[A-Za-z]+\b', uni['name'].lower())
        name_words.extend(words)
    
    common_words = Counter(name_words).most_common(20)
    print("Most common words in university names:")
    for word, count in common_words:
        print(f"  {word}: {count}")
    
    # Analyze web address patterns
    print("\n" + "="*80)
    print("\nAnalyzing web address patterns:")
    domains = []
    for uni in unknown_universities:
        if uni['web_address']:
            # Extract domain from URL
            match = re.search(r'https?://[^/]+', uni['web_address'])
            if match:
                domains.append(match.group())
    
    domain_counter = Counter(domains).most_common(10)
    print("Most common domains:")
    for domain, count in domain_counter:
        print(f"  {domain}: {count}")
    
    # Show sample universities by country patterns
    print("\n" + "="*80)
    print("\nSample universities with 'Unknown' country:")
    
    # Group by potential country indicators
    country_indicators = {
        'Germany': ['berlin', 'munich', 'hamburg', 'cologne', 'frankfurt', 'stuttgart', 'dresden', 'leipzig'],
        'Japan': ['tokyo', 'osaka', 'kyoto', 'nagoya', 'hiroshima', 'sendai', 'fukuoka', 'sapporo'],
        'China': ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'nanjing', 'hangzhou', 'wuhan', 'chengdu'],
        'India': ['delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad'],
        'Italy': ['rome', 'milan', 'naples', 'turin', 'florence', 'bologna', 'venice', 'genoa'],
        'Spain': ['madrid', 'barcelona', 'valencia', 'seville', 'bilbao', 'zaragoza', 'malaga'],
        'France': ['paris', 'lyon', 'marseille', 'toulouse', 'nice', 'nantes', 'strasbourg'],
        'Netherlands': ['amsterdam', 'rotterdam', 'utrecht', 'eindhoven', 'tilburg', 'groningen'],
        'Belgium': ['brussels', 'antwerp', 'ghent', 'bruges', 'leuven', 'liege'],
        'Switzerland': ['zurich', 'geneva', 'basel', 'bern', 'lausanne'],
        'Austria': ['vienna', 'salzburg', 'innsbruck', 'graz', 'linz'],
        'Sweden': ['stockholm', 'gothenburg', 'malmo', 'uppsala', 'linkoping'],
        'Norway': ['oslo', 'bergen', 'trondheim', 'stavanger'],
        'Denmark': ['copenhagen', 'aarhus', 'odense', 'aalborg'],
        'Finland': ['helsinki', 'tampere', 'turku', 'oulu'],
        'Poland': ['warsaw', 'krakow', 'gdansk', 'wroclaw', 'poznan'],
        'Czech Republic': ['prague', 'brno', 'ostrava'],
        'Hungary': ['budapest', 'debrecen', 'szeged'],
        'Portugal': ['lisbon', 'porto', 'coimbra'],
        'Greece': ['athens', 'thessaloniki', 'patras'],
        'Turkey': ['istanbul', 'ankara', 'izmir', 'bursa'],
        'Russia': ['moscow', 'st petersburg', 'novosibirsk', 'yekaterinburg'],
        'South Korea': ['seoul', 'busan', 'incheon', 'daegu', 'daejeon'],
        'Taiwan': ['taipei', 'kaohsiung', 'taichung', 'tainan'],
        'Thailand': ['bangkok', 'chiang mai', 'phuket'],
        'Malaysia': ['kuala lumpur', 'penang', 'johor'],
        'Singapore': ['singapore'],
        'Indonesia': ['jakarta', 'surabaya', 'bandung', 'medan'],
        'Philippines': ['manila', 'cebu', 'davao'],
        'Vietnam': ['hanoi', 'ho chi minh', 'da nang'],
        'Iran': ['tehran', 'isfahan', 'mashhad', 'tabriz'],
        'Israel': ['jerusalem', 'tel aviv', 'haifa'],
        'Egypt': ['cairo', 'alexandria', 'giza'],
        'South Africa': ['cape town', 'johannesburg', 'durban', 'pretoria'],
        'Nigeria': ['lagos', 'abuja', 'kano', 'ibadan'],
        'Kenya': ['nairobi', 'mombasa'],
        'Ghana': ['accra', 'kumasi'],
        'Morocco': ['casablanca', 'rabat', 'fez'],
        'Brazil': ['sao paulo', 'rio de janeiro', 'brasilia', 'salvador'],
        'Argentina': ['buenos aires', 'cordoba', 'rosario'],
        'Chile': ['santiago', 'valparaiso'],
        'Colombia': ['bogota', 'medellin', 'cali'],
        'Mexico': ['mexico city', 'guadalajara', 'monterrey'],
        'Peru': ['lima', 'arequipa', 'cusco']
    }
    
    for country, cities in country_indicators.items():
        matching_unis = []
        for uni in unknown_universities:
            name_lower = uni['name'].lower()
            desc_lower = uni['description'].lower()
            for city in cities:
                if city in name_lower or city in desc_lower:
                    matching_unis.append(uni['name'])
                    break
        
        if matching_unis:
            print(f"\n{country} ({len(matching_unis)} universities):")
            for name in matching_unis[:5]:  # Show first 5
                print(f"  - {name}")
            if len(matching_unis) > 5:
                print(f"  ... and {len(matching_unis) - 5} more")
    
    print("\n" + "="*80)
    print("\nFirst 20 universities with 'Unknown' country:")
    for i, uni in enumerate(unknown_universities[:20]):
        print(f"{i+1:2d}. {uni['name']}")
        if uni['description']:
            print(f"    Description: {uni['description']}")
        print()

if __name__ == "__main__":
    analyze_unknown_countries()