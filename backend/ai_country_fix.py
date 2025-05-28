#!/usr/bin/env python3
import json
import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def ai_country_fix():
    # Check for OpenRouter API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        print("Please add your OpenRouter API key to the .env file:")
        print("OPENROUTER_API_KEY=your_api_key_here")
        return
    
    # Load the JSON data
    with open('updated_universities_fixed.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    # Country code mapping
    country_codes = {
        'united states': 'US', 'germany': 'DE', 'italy': 'IT', 'spain': 'ES', 'france': 'FR',
        'netherlands': 'NL', 'belgium': 'BE', 'switzerland': 'CH', 'austria': 'AT',
        'sweden': 'SE', 'norway': 'NO', 'denmark': 'DK', 'finland': 'FI', 'poland': 'PL',
        'czech republic': 'CZ', 'hungary': 'HU', 'portugal': 'PT', 'greece': 'GR',
        'turkey': 'TR', 'russia': 'RU', 'japan': 'JP', 'south korea': 'KR', 'china': 'CN',
        'taiwan': 'TW', 'hong kong': 'HK', 'singapore': 'SG', 'malaysia': 'MY',
        'thailand': 'TH', 'indonesia': 'ID', 'philippines': 'PH', 'vietnam': 'VN',
        'india': 'IN', 'iran': 'IR', 'israel': 'IL', 'egypt': 'EG', 'south africa': 'ZA',
        'nigeria': 'NG', 'kenya': 'KE', 'ghana': 'GH', 'morocco': 'MA', 'brazil': 'BR',
        'argentina': 'AR', 'chile': 'CL', 'colombia': 'CO', 'mexico': 'MX', 'peru': 'PE',
        'canada': 'CA', 'australia': 'AU', 'new zealand': 'NZ', 'united kingdom': 'GB',
        'ireland': 'IE', 'croatia': 'HR', 'slovenia': 'SI', 'slovakia': 'SK', 'romania': 'RO',
        'bulgaria': 'BG', 'serbia': 'RS', 'bosnia and herzegovina': 'BA', 'montenegro': 'ME',
        'north macedonia': 'MK', 'albania': 'AL', 'estonia': 'EE', 'latvia': 'LV',
        'lithuania': 'LT', 'ukraine': 'UA', 'belarus': 'BY', 'moldova': 'MD',
        'georgia': 'GE', 'armenia': 'AM', 'azerbaijan': 'AZ', 'kazakhstan': 'KZ',
        'uzbekistan': 'UZ', 'kyrgyzstan': 'KG', 'tajikistan': 'TJ', 'turkmenistan': 'TM',
        'afghanistan': 'AF', 'pakistan': 'PK', 'bangladesh': 'BD', 'sri lanka': 'LK',
        'nepal': 'NP', 'bhutan': 'BT', 'maldives': 'MV', 'myanmar': 'MM', 'laos': 'LA',
        'cambodia': 'KH', 'brunei': 'BN', 'timor-leste': 'TL', 'papua new guinea': 'PG',
        'fiji': 'FJ', 'solomon islands': 'SB', 'vanuatu': 'VU', 'samoa': 'WS',
        'tonga': 'TO', 'kiribati': 'KI', 'tuvalu': 'TV', 'nauru': 'NR', 'palau': 'PW',
        'marshall islands': 'MH', 'micronesia': 'FM', 'lebanon': 'LB', 'syria': 'SY',
        'jordan': 'JO', 'iraq': 'IQ', 'kuwait': 'KW', 'saudi arabia': 'SA',
        'bahrain': 'BH', 'qatar': 'QA', 'united arab emirates': 'AE', 'oman': 'OM',
        'yemen': 'YE', 'libya': 'LY', 'tunisia': 'TN', 'algeria': 'DZ', 'sudan': 'SD',
        'south sudan': 'SS', 'ethiopia': 'ET', 'eritrea': 'ER', 'djibouti': 'DJ',
        'somalia': 'SO', 'uganda': 'UG', 'tanzania': 'TZ', 'rwanda': 'RW',
        'burundi': 'BI', 'democratic republic of congo': 'CD', 'republic of congo': 'CG',
        'central african republic': 'CF', 'chad': 'TD', 'cameroon': 'CM',
        'equatorial guinea': 'GQ', 'gabon': 'GA', 'sao tome and principe': 'ST',
        'cape verde': 'CV', 'guinea-bissau': 'GW', 'guinea': 'GN', 'sierra leone': 'SL',
        'liberia': 'LR', 'ivory coast': 'CI', 'burkina faso': 'BF', 'mali': 'ML',
        'niger': 'NE', 'senegal': 'SN', 'gambia': 'GM', 'mauritania': 'MR',
        'madagascar': 'MG', 'mauritius': 'MU', 'seychelles': 'SC', 'comoros': 'KM',
        'botswana': 'BW', 'namibia': 'NA', 'zambia': 'ZM', 'zimbabwe': 'ZW',
        'malawi': 'MW', 'mozambique': 'MZ', 'swaziland': 'SZ', 'lesotho': 'LS',
        'uruguay': 'UY', 'paraguay': 'PY', 'bolivia': 'BO', 'ecuador': 'EC',
        'venezuela': 'VE', 'guyana': 'GY', 'suriname': 'SR', 'french guiana': 'GF',
        'costa rica': 'CR', 'panama': 'PA', 'nicaragua': 'NI', 'honduras': 'HN',
        'el salvador': 'SV', 'guatemala': 'GT', 'belize': 'BZ', 'jamaica': 'JM',
        'haiti': 'HT', 'dominican republic': 'DO', 'cuba': 'CU', 'bahamas': 'BS',
        'barbados': 'BB', 'trinidad and tobago': 'TT', 'grenada': 'GD',
        'saint vincent and the grenadines': 'VC', 'saint lucia': 'LC',
        'dominica': 'DM', 'antigua and barbuda': 'AG', 'saint kitts and nevis': 'KN'
    }
    
    def get_country_from_ai(university_name, web_address, description=""):
        """Use OpenRouter with Google Gemma to determine the country of a university"""
        prompt = f"""
        Identify the country for this university. Respond with ONLY the country name in lowercase (e.g., "united states", "germany", "japan").
        
        University Name: {university_name}
        Web Address: {web_address}
        Description: {description}
        
        Based on the university name, web domain, and any other context clues, what country is this university located in?
        Respond with only the country name in lowercase, no explanation.
        """
        
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "google/gemma-2-9b-it:free",
                    "messages": [
                        {"role": "system", "content": "You are a geography expert specializing in identifying university locations. Respond only with the country name in lowercase."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 50,
                    "temperature": 0.1
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                country = result['choices'][0]['message']['content'].strip().lower()
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return None, None
            
            # Clean up common variations
            country_mappings = {
                'usa': 'united states',
                'us': 'united states',
                'america': 'united states',
                'uk': 'united kingdom',
                'britain': 'united kingdom',
                'england': 'united kingdom',
                'south korea': 'south korea',
                'korea': 'south korea',
                'prc': 'china',
                'people\'s republic of china': 'china',
                'roc': 'taiwan',
                'republic of china': 'taiwan',
                'uae': 'united arab emirates',
                'drc': 'democratic republic of congo',
                'congo': 'democratic republic of congo'
            }
            
            country = country_mappings.get(country, country)
            
            if country in country_codes:
                return country, country_codes[country]
            else:
                print(f"Warning: Unknown country '{country}' returned by AI for {university_name}")
                return None, None
                
        except Exception as e:
            print(f"Error calling OpenRouter API for {university_name}: {e}")
            return None, None
    
    # Find universities with Unknown country
    unknown_universities = []
    for i, university in enumerate(universities):
        if university.get('country') == 'Unknown':
            unknown_universities.append((i, university))
    
    print(f"Found {len(unknown_universities)} universities with Unknown country")
    
    if len(unknown_universities) == 0:
        print("No universities with Unknown country found.")
        return
    
    # Process in batches to avoid rate limits
    batch_size = 10
    fixed_count = 0
    
    for i in range(0, len(unknown_universities), batch_size):
        batch = unknown_universities[i:i+batch_size]
        
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(unknown_universities)-1)//batch_size + 1}...")
        
        for idx, university in batch:
            name = university.get('name', '')
            web_address = university.get('web_address', '')
            description = university.get('description', '')
            
            print(f"Processing: {name}")
            
            country, country_code = get_country_from_ai(name, web_address, description)
            
            if country and country_code:
                universities[idx]['country'] = country.title()
                universities[idx]['country_code'] = country_code
                print(f"  ✅ Fixed: {name} -> {country.title()} ({country_code})")
                fixed_count += 1
            else:
                print(f"  ❌ Could not determine country for: {name}")
            
            # Add delay to respect rate limits
            time.sleep(1)
        
        # Longer delay between batches
        if i + batch_size < len(unknown_universities):
            print("Waiting 5 seconds before next batch...")
            time.sleep(5)
    
    print(f"\n=== AI COUNTRY FIX COMPLETED ===")
    print(f"Fixed {fixed_count} universities with AI assistance")
    
    # Save the updated JSON
    output_file = 'updated_universities_ai_fixed.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(universities, f, indent=2, ensure_ascii=False)
    
    print(f"Updated JSON saved to: {output_file}")
    
    # Show final statistics
    total_universities = len(universities)
    unknown_count = sum(1 for uni in universities if uni.get('country') == 'Unknown')
    known_count = total_universities - unknown_count
    
    print(f"\n=== FINAL STATISTICS ===")
    print(f"Total universities: {total_universities}")
    print(f"Known countries: {known_count} ({known_count/total_universities*100:.1f}%)")
    print(f"Unknown countries: {unknown_count} ({unknown_count/total_universities*100:.1f}%)")
    
if __name__ == "__main__":
    ai_country_fix()