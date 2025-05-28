#!/usr/bin/env python3

import json
import re
from typing import Dict, List, Any, Optional

def infer_country_from_university_data(university: Dict[str, Any]) -> tuple[str, str]:
    """Infer country and country code from university name and web address"""
    
    name = university.get('name', '').lower()
    web_address = university.get('web_address', '').lower()
    
    # Country patterns in university names
    name_patterns = {
        'united states': ['university of california', 'california institute', 'stanford', 'harvard', 'mit', 'yale', 
                         'princeton', 'columbia', 'university of chicago', 'northwestern', 'duke', 'cornell',
                         'university of pennsylvania', 'johns hopkins', 'dartmouth', 'brown', 'rice',
                         'vanderbilt', 'emory', 'georgetown', 'carnegie mellon', 'university of michigan',
                         'university of virginia', 'university of north carolina', 'georgia institute',
                         'university of wisconsin', 'university of illinois', 'university of washington',
                         'university of texas', 'university of florida', 'ohio state', 'penn state',
                         'michigan state', 'purdue', 'indiana university', 'university of minnesota',
                         'university of colorado', 'arizona state', 'university of arizona', 'rutgers',
                         'university of maryland', 'virginia tech', 'texas a&m', 'university of georgia',
                         'university of iowa', 'university of kansas', 'university of missouri',
                         'university of nebraska', 'university of oklahoma', 'university of oregon',
                         'university of utah', 'washington university', 'boston university', 'northeastern',
                         'new york university', 'fordham', 'syracuse', 'university of rochester',
                         'case western', 'tulane', 'wake forest', 'lehigh', 'rensselaer', 'worcester',
                         'california state', 'san diego state', 'florida state', 'north carolina state',
                         'virginia commonwealth', 'george washington', 'american university',
                         'university of denver', 'university of miami', 'university of southern california',
                         ],
        'united kingdom': ['university of oxford', 'university of cambridge', 'imperial college', 'university college london',
                          'london school of economics', 'kings college london', 'university of edinburgh',
                          'university of manchester', 'university of bristol', 'university of warwick',
                          'university of glasgow', 'university of birmingham', 'university of sheffield',
                          'university of nottingham', 'university of southampton', 'university of leeds',
                          'university of liverpool', 'university of york', 'university of exeter',
                          'university of bath', 'university of durham', 'university of st andrews',
                          'university of leicester', 'university of surrey', 'university of sussex',
                          'university of east anglia', 'university of kent', 'university of reading',
                          'university of hull', 'university of portsmouth', 'university of plymouth',
                          'university of hertfordshire', 'university of greenwich', 'university of westminster',
                          'brunel university', 'middlesex university', 'city university', 'goldsmiths'],
        'canada': ['university of toronto', 'university of british columbia', 'mcgill university',
                  'university of alberta', 'university of montreal', 'university of waterloo',
                  'queens university', 'university of calgary', 'university of ottawa',
                  'university of manitoba', 'university of saskatchewan', 'dalhousie university',
                  'university of victoria', 'simon fraser university', 'carleton university',
                  'concordia university', 'york university', 'ryerson university', 'university of guelph',
                   'mcmaster university'],
        'australia': ['university of melbourne', 'university of sydney', 'australian national university',
                     'university of queensland', 'university of new south wales', 'monash university',
                     'university of western australia', 'university of adelaide', 'macquarie university',
                     'university of technology sydney', 'queensland university of technology',
                     'deakin university', 'griffith university', 'la trobe university', 'rmit university',
                     'unsw sydney', 'unsw', 'university of new south wales sydney'],
        'germany': ['technical university of munich', 'ludwig maximilian university', 'heidelberg university',
                   'humboldt university', 'university of freiburg', 'university of gottingen',
                   'university of hamburg', 'university of cologne', 'university of bonn',
                   'karlsruhe institute of technology', 'rwth aachen', 'technical university of berlin',
                   'university of tubingen', 'university of wurzburg', 'university of munster',
                   'lmu munich', 'charité', 'universitätsmedizin berlin',
                   'charité - universitätsmedizin berlin', 'technical university of darmstadt',
                   'university of ulm', 'university of greifswald', 'university of rostock'],
        'france': ['sorbonne university', 'ecole normale superieure', 'ecole polytechnique',
                  'university of paris', 'sciences po', 'insead', 'hec paris', 'centrale supelec'],
        'netherlands': ['university of amsterdam', 'delft university of technology', 'utrecht university',
                       'leiden university', 'eindhoven university', 'university of groningen',
                       'erasmus university', 'vrije universiteit amsterdam', 'wageningen university'],
        'switzerland': ['eth zurich', 'epfl', 'university of zurich', 'university of geneva',
                       'university of basel', 'university of bern', 'university of lausanne'],
        'sweden': ['karolinska institute', 'royal institute of technology', 'stockholm university',
                  'lund university', 'university of gothenburg', 'uppsala university'],
        'denmark': ['university of copenhagen', 'technical university of denmark', 'aarhus university'],
        'norway': ['university of oslo', 'norwegian university of science and technology'],
        'finland': ['university of helsinki', 'aalto university'],
        'belgium': ['ku leuven', 'ghent university', 'universite libre de bruxelles'],
        'austria': ['university of vienna', 'vienna university of technology'],
        'italy': ['university of bologna', 'sapienza university of rome', 'university of milan'],
        'spain': ['university of barcelona', 'autonomous university of madrid', 'complutense university'],
        'japan': ['university of tokyo', 'kyoto university', 'osaka university', 'tohoku university',
                 'nagoya university', 'hokkaido university', 'kyushu university', 'tokyo institute of technology',
                 'waseda university', 'keio university'],
        'south korea': ['seoul national university', 'kaist', 'postech', 'yonsei university', 'korea university'],
        'china': ['tsinghua university', 'peking university', 'fudan university', 'shanghai jiao tong university',
                 'zhejiang university', 'university of science and technology of china', 'nanjing university',
                 'wuhan university', 'sun yat-sen university', 'beihang university', 'beijing normal university'],
        'hong kong': ['university of hong kong', 'chinese university of hong kong', 'hong kong university of science'],
        'singapore': ['national university of singapore', 'nanyang technological university'],
        'new zealand': ['university of auckland', 'university of otago'],
        'ireland': ['trinity college dublin', 'university college dublin'],
        'israel': ['hebrew university', 'technion', 'tel aviv university'],
        'brazil': ['university of sao paulo', 'university of campinas'],
        'chile': ['pontificia universidad catolica de chile', 'universidad de chile'],
        'mexico': ['universidad nacional autonoma de mexico'],
        'south africa': ['university of cape town', 'university of witwatersrand'],
        'india': ['indian institute of science', 'indian institute of technology'],
        'thailand': ['chulalongkorn university'],
        'malaysia': ['university of malaya'],
        'taiwan': ['national taiwan university'],
        'russia': ['moscow state university', 'saint petersburg state university'],
        'poland': ['university of warsaw'],
        'czech republic': ['charles university'],
        'hungary': ['eotvos lorand university'],
        'portugal': ['university of porto'],
        'greece': ['national technical university of athens'],
        'turkey': ['middle east technical university', 'bogazici university', 'istanbul technical university'],
        'indonesia': ['gadjah mada university', 'universitas gadjah mada', 'university of indonesia', 'universitas indonesia', 'institut teknologi bandung', 'universitas airlangga', 'universitas brawijaya', 'universitas diponegoro', 'universitas hasanuddin', 'universitas padjadjaran', 'universitas sebelas maret', 'universitas sumatera utara', 'universitas udayana', 'universitas andalas'],
        'philippines': ['university of the philippines', 'ateneo de manila university', 'de la salle university'],
        'vietnam': ['vietnam national university', 'hanoi university of science and technology'],
        'egypt': ['cairo university', 'american university in cairo', 'alexandria university'],
        'saudi arabia': ['king abdulaziz university', 'king saud university', 'king fahd university'],
        'uae': ['american university of sharjah', 'united arab emirates university'],
        'lebanon': ['american university of beirut', 'lebanese american university'],
        'jordan': ['university of jordan', 'jordan university of science'],
        'morocco': ['mohammed v university', 'al akhawayn university'],
        'tunisia': ['university of tunis'],
        'kenya': ['university of nairobi', 'kenyatta university'],
        'nigeria': ['university of ibadan', 'university of lagos'],
        'ghana': ['university of ghana'],
        'argentina': ['university of buenos aires', 'universidad de buenos aires'],
        'colombia': ['universidad nacional de colombia', 'universidad de los andes'],
        'peru': ['pontificia universidad catolica del peru'],
        'venezuela': ['universidad central de venezuela'],
        'ecuador': ['pontificia universidad javeriana'],
        'uruguay': ['universidad de la republica'],
        'pakistan': ['university of karachi', 'lahore university of management'],
        'bangladesh': ['university of dhaka', 'bangladesh university of engineering'],
        'sri lanka': ['university of colombo', 'university of peradeniya'],
        'nepal': ['tribhuvan university'],
        'iran': ['university of tehran', 'sharif university of technology'],
        'iraq': ['university of baghdad'],
        'kuwait': ['kuwait university'],
        'qatar': ['qatar university'],
        'bahrain': ['university of bahrain'],
        'oman': ['sultan qaboos university'],
        'yemen': ['sana\'a university'],
        'afghanistan': ['kabul university'],
        'uzbekistan': ['national university of uzbekistan'],
        'kazakhstan': ['al-farabi kazakh national university'],
        'kyrgyzstan': ['kyrgyz national university'],
        'tajikistan': ['tajik national university'],
        'turkmenistan': ['magtymguly turkmen state university'],
        'mongolia': ['national university of mongolia'],
        'myanmar': ['university of yangon'],
        'cambodia': ['royal university of phnom penh'],
        'laos': ['national university of laos'],
        'brunei': ['universiti brunei darussalam'],
        'maldives': ['maldives national university'],
        'bhutan': ['royal university of bhutan'],
        'fiji': ['university of the south pacific'],
        'papua new guinea': ['university of papua new guinea'],
        'solomon islands': ['solomon islands national university'],
        'vanuatu': ['university of the south pacific'],
        'samoa': ['national university of samoa'],
        'tonga': ['university of the south pacific'],
        'palau': ['palau community college'],
        'micronesia': ['college of micronesia'],
        'marshall islands': ['college of the marshall islands'],
        'kiribati': ['university of the south pacific'],
        'tuvalu': ['university of the south pacific'],
        'nauru': ['university of the south pacific']
    }
    
    # Web address patterns
    web_patterns = {
        'united states': ['.edu', 'caltech.edu', 'mit.edu', 'harvard.edu', 'stanford.edu'],
        'united kingdom': ['.ac.uk', '.uk'],
        'canada': ['.ca'],
        'australia': ['.edu.au', '.au'],
        'germany': ['.de'],
        'france': ['.fr'],
        'netherlands': ['.nl'],
        'switzerland': ['.ch'],
        'sweden': ['.se'],
        'denmark': ['.dk'],
        'norway': ['.no'],
        'finland': ['.fi'],
        'belgium': ['.be'],
        'austria': ['.at'],
        'italy': ['.it'],
        'spain': ['.es'],
        'japan': ['.jp'],
        'south korea': ['.kr'],
        'china': ['.cn'],
        'hong kong': ['.hk'],
        'singapore': ['.sg'],
        'new zealand': ['.nz'],
        'ireland': ['.ie'],
        'israel': ['.il'],
        'brazil': ['.br'],
        'chile': ['.cl'],
        'mexico': ['.mx'],
        'south africa': ['.za'],
        'india': ['.in'],
        'thailand': ['.th'],
        'malaysia': ['.my'],
        'taiwan': ['.tw'],
        'russia': ['.ru'],
        'poland': ['.pl'],
        'czech republic': ['.cz'],
        'hungary': ['.hu'],
        'portugal': ['.pt'],
        'greece': ['.gr'],
        'turkey': ['.tr'],
        'indonesia': ['.id'],
        'philippines': ['.ph'],
        'vietnam': ['.vn'],
        'egypt': ['.eg'],
        'saudi arabia': ['.sa'],
        'uae': ['.ae'],
        'lebanon': ['.lb'],
        'jordan': ['.jo'],
        'morocco': ['.ma'],
        'tunisia': ['.tn'],
        'kenya': ['.ke'],
        'nigeria': ['.ng'],
        'ghana': ['.gh'],
        'argentina': ['.ar'],
        'colombia': ['.co'],
        'peru': ['.pe'],
        'venezuela': ['.ve'],
        'ecuador': ['.ec'],
        'uruguay': ['.uy'],
        'pakistan': ['.pk'],
        'bangladesh': ['.bd'],
        'sri lanka': ['.lk'],
        'nepal': ['.np'],
        'iran': ['.ir'],
        'iraq': ['.iq'],
        'kuwait': ['.kw'],
        'qatar': ['.qa'],
        'bahrain': ['.bh'],
        'oman': ['.om'],
        'yemen': ['.ye'],
        'afghanistan': ['.af'],
        'uzbekistan': ['.uz'],
        'kazakhstan': ['.kz'],
        'kyrgyzstan': ['.kg'],
        'tajikistan': ['.tj'],
        'turkmenistan': ['.tm'],
        'mongolia': ['.mn'],
        'myanmar': ['.mm'],
        'cambodia': ['.kh'],
        'laos': ['.la'],
        'brunei': ['.bn'],
        'maldives': ['.mv'],
        'bhutan': ['.bt'],
        'fiji': ['.fj'],
        'papua new guinea': ['.pg'],
        'solomon islands': ['.sb'],
        'vanuatu': ['.vu'],
        'samoa': ['.ws'],
        'tonga': ['.to'],
        'palau': ['.pw'],
        'micronesia': ['.fm'],
        'marshall islands': ['.mh'],
        'kiribati': ['.ki'],
        'tuvalu': ['.tv'],
        'nauru': ['.nr']
    }
    
    # Country code mapping
    country_codes = {
        'united states': 'US',
        'united kingdom': 'UK',
        'canada': 'CA',
        'australia': 'AU',
        'germany': 'DE',
        'france': 'FR',
        'netherlands': 'NL',
        'switzerland': 'CH',
        'sweden': 'SE',
        'denmark': 'DK',
        'norway': 'NO',
        'finland': 'FI',
        'belgium': 'BE',
        'austria': 'AT',
        'italy': 'IT',
        'spain': 'ES',
        'japan': 'JP',
        'south korea': 'KR',
        'china': 'CN',
        'hong kong': 'HK',
        'singapore': 'SG',
        'new zealand': 'NZ',
        'ireland': 'IE',
        'israel': 'IL',
        'brazil': 'BR',
        'chile': 'CL',
        'mexico': 'MX',
        'south africa': 'ZA',
        'india': 'IN',
        'thailand': 'TH',
        'malaysia': 'MY',
        'taiwan': 'TW',
        'russia': 'RU',
        'poland': 'PL',
        'czech republic': 'CZ',
        'hungary': 'HU',
        'portugal': 'PT',
        'greece': 'GR',
        'turkey': 'TR',
        'indonesia': 'ID',
        'philippines': 'PH',
        'vietnam': 'VN',
        'egypt': 'EG',
        'saudi arabia': 'SA',
        'uae': 'AE',
        'lebanon': 'LB',
        'jordan': 'JO',
        'morocco': 'MA',
        'tunisia': 'TN',
        'kenya': 'KE',
        'nigeria': 'NG',
        'ghana': 'GH',
        'argentina': 'AR',
        'colombia': 'CO',
        'peru': 'PE',
        'venezuela': 'VE',
        'ecuador': 'EC',
        'uruguay': 'UY',
        'pakistan': 'PK',
        'bangladesh': 'BD',
        'sri lanka': 'LK',
        'nepal': 'NP',
        'iran': 'IR',
        'iraq': 'IQ',
        'kuwait': 'KW',
        'qatar': 'QA',
        'bahrain': 'BH',
        'oman': 'OM',
        'yemen': 'YE',
        'afghanistan': 'AF',
        'uzbekistan': 'UZ',
        'kazakhstan': 'KZ',
        'kyrgyzstan': 'KG',
        'tajikistan': 'TJ',
        'turkmenistan': 'TM',
        'mongolia': 'MN',
        'myanmar': 'MM',
        'cambodia': 'KH',
        'laos': 'LA',
        'brunei': 'BN',
        'maldives': 'MV',
        'bhutan': 'BT',
        'fiji': 'FJ',
        'papua new guinea': 'PG',
        'solomon islands': 'SB',
        'vanuatu': 'VU',
        'samoa': 'WS',
        'tonga': 'TO',
        'palau': 'PW',
        'micronesia': 'FM',
        'marshall islands': 'MH',
        'kiribati': 'KI',
        'tuvalu': 'TV',
        'nauru': 'NR'
    }
    
    # Check name patterns first
    for country, patterns in name_patterns.items():
        for pattern in patterns:
            if pattern in name:
                return country.title(), country_codes[country]
    
    # Check web address patterns (more specific matching)
    for country, patterns in web_patterns.items():
        for pattern in patterns:
            # For domain extensions, ensure they are at the end or followed by a slash/query
            if pattern.startswith('.'):
                if web_address.endswith(pattern) or f'{pattern}/' in web_address or f'{pattern}?' in web_address:
                    return country.title(), country_codes[country]
            else:
                if pattern in web_address:
                    return country.title(), country_codes[country]
    
    # Default fallback
    return 'Unknown', ''

def fix_null_countries_in_json(input_file: str, output_file: str):
    """Fix null country values in the JSON file"""
    
    # Load the JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    print(f"Loaded {len(universities)} universities")
    
    fixed_count = 0
    
    for university in universities:
        if university.get('country') is None or university.get('country_code') is None:
            country, country_code = infer_country_from_university_data(university)
            
            if country != 'Unknown':
                university['country'] = country
                university['country_code'] = country_code
                fixed_count += 1
                print(f"Fixed: {university.get('name', 'Unknown')} -> {country} ({country_code})")
            else:
                # Set to Unknown if we can't determine
                university['country'] = 'Unknown'
                university['country_code'] = ''
                print(f"Could not determine country for: {university.get('name', 'Unknown')}")
    
    # Save the fixed JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(universities, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} universities with null countries")
    print(f"Updated JSON saved to: {output_file}")

def main():
    input_file = "/Users/wisemaker/Sites/university-recommender/backend/updated_universities.json"
    output_file = "/Users/wisemaker/Sites/university-recommender/backend/updated_universities_fixed.json"
    
    fix_null_countries_in_json(input_file, output_file)

if __name__ == "__main__":
    main()