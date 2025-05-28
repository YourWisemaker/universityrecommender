#!/usr/bin/env python3
import json
import re

def comprehensive_country_fix():
    # Load the JSON data
    with open('updated_universities_fixed.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)
    
    # Comprehensive university name patterns for specific countries
    university_patterns = {
        'united states': [
            'university of california', 'stanford university', 'harvard university', 'mit',
            'massachusetts institute of technology', 'yale university', 'princeton university',
            'columbia university', 'university of chicago', 'university of pennsylvania',
            'cornell university', 'dartmouth college', 'brown university', 'duke university',
            'northwestern university', 'johns hopkins university', 'washington university',
            'rice university', 'vanderbilt university', 'emory university', 'georgetown university',
            'carnegie mellon university', 'university of southern california', 'wake forest university',
            'university of virginia', 'university of michigan', 'university of north carolina',
            'georgia institute of technology', 'university of rochester', 'brandeis university',
            'case western reserve university', 'new york university', 'boston university',
            'tulane university', 'university of miami', 'university of wisconsin',
            'pennsylvania state university', 'university of illinois', 'ohio state university',
            'university of washington', 'university of texas', 'university of florida',
            'university of georgia', 'university of minnesota', 'purdue university',
            'michigan state university', 'university of iowa', 'indiana university',
            'university of colorado', 'arizona state university', 'university of arizona',
            'university of utah', 'university of oregon', 'oregon state university',
            'california institute of technology', 'caltech'
        ],
        'germany': [
            'technical university of munich', 'ludwig maximilian university', 'heidelberg university',
            'humboldt university', 'university of freiburg', 'university of gottingen',
            'university of hamburg', 'university of cologne', 'university of bonn',
            'karlsruhe institute of technology', 'rwth aachen', 'technical university of berlin',
            'university of tubingen', 'university of wurzburg', 'university of munster',
            'lmu munich', 'charité', 'universitätsmedizin berlin',
            'charité - universitätsmedizin berlin', 'technical university of darmstadt',
            'university of ulm', 'university of greifswald', 'university of rostock',
            'university of mannheim', 'tu dresden', 'dresden university of technology',
            'technical university of dresden', 'university of frankfurt', 'goethe university',
            'university of stuttgart', 'university of leipzig', 'university of jena',
            'university of kiel', 'university of bremen', 'university of hannover',
            'university of dortmund', 'ruhr university bochum', 'university of duisburg-essen',
            'university of bielefeld', 'university of konstanz', 'university of regensburg',
            'university of bayreuth', 'university of passau', 'university of augsburg',
            'university of bamberg', 'free university of berlin', 'technical university of kaiserslautern'
        ],
        'italy': [
            'university of bologna', 'sapienza university of rome', 'university of milan',
            'university of florence', 'university of turin', 'university of naples',
            'university of padua', 'university of pisa', 'university of genoa',
            'university of rome', 'bocconi university', 'polytechnic university of milan',
            'scuola normale superiore', 'sant\'anna school of advanced studies',
            'university of venice', 'university of verona', 'university of trieste',
            'university of bari', 'university of palermo', 'university of catania',
            'university of cagliari', 'university of perugia', 'university of siena',
            'university of parma', 'university of modena', 'university of ferrara',
            'scuola normale superiore di pisa', 'università bocconi'
        ],
        'spain': [
            'university of barcelona', 'autonomous university of barcelona', 'complutense university of madrid',
            'autonomous university of madrid', 'university of valencia', 'university of seville',
            'university of granada', 'university of zaragoza', 'university of santiago de compostela',
            'university of the basque country', 'polytechnic university of catalonia',
            'polytechnic university of madrid', 'university of oviedo', 'university of murcia',
            'university of alicante', 'university of vigo', 'university of salamanca',
            'university of valladolid', 'university of córdoba', 'university of extremadura',
            'universitat autònoma de barcelona', 'uab', 'universitat de barcelona',
            'universidad complutense de madrid', 'universidad autónoma de madrid'
        ],
        'france': [
            'sorbonne university', 'ecole normale superieure', 'ecole polytechnique',
            'university of paris', 'sciences po', 'insead', 'hec paris', 'centrale supelec',
            'université paris-saclay', 'université psl', 'université sorbonne paris nord',
            'université de lyon', 'université de marseille', 'université de toulouse',
            'université de bordeaux', 'université de lille', 'université de nantes',
            'université de strasbourg', 'université de montpellier', 'université de nice',
            'école normale supérieure', 'école polytechnique', 'université paris-sorbonne',
            'université pierre et marie curie', 'université paris diderot'
        ],
        'netherlands': [
            'university of amsterdam', 'delft university of technology', 'utrecht university',
            'leiden university', 'erasmus university rotterdam', 'university of groningen',
            'eindhoven university of technology', 'vrije universiteit amsterdam',
            'wageningen university', 'tilburg university', 'maastricht university',
            'radboud university', 'university of twente', 'amsterdam university of applied sciences'
        ],
        'belgium': [
            'ku leuven', 'ghent university', 'université libre de bruxelles',
            'university of antwerp', 'vrije universiteit brussel', 'université catholique de louvain',
            'university of liège', 'hasselt university'
        ],
        'switzerland': [
            'eth zurich', 'university of zurich', 'university of geneva', 'university of basel',
            'university of bern', 'university of lausanne', 'epfl', 'university of fribourg',
            'university of neuchâtel', 'university of st gallen'
        ],
        'austria': [
            'university of vienna', 'vienna university of technology', 'university of graz',
            'university of innsbruck', 'university of salzburg', 'university of linz',
            'vienna university of economics and business'
        ],
        'sweden': [
            'karolinska institute', 'royal institute of technology', 'stockholm university',
            'university of gothenburg', 'lund university', 'uppsala university',
            'chalmers university of technology', 'linköping university', 'umeå university'
        ],
        'norway': [
            'university of oslo', 'norwegian university of science and technology',
            'university of bergen', 'university of tromsø', 'norwegian school of economics'
        ],
        'denmark': [
            'university of copenhagen', 'technical university of denmark', 'aarhus university',
            'university of southern denmark', 'aalborg university', 'copenhagen business school'
        ],
        'finland': [
            'university of helsinki', 'aalto university', 'university of turku',
            'university of tampere', 'university of oulu', 'university of jyväskylä'
        ],
        'poland': [
            'university of warsaw', 'jagiellonian university', 'warsaw university of technology',
            'university of krakow', 'adam mickiewicz university', 'university of wrocław',
            'gdansk university of technology', 'poznan university of technology'
        ],
        'czech republic': [
            'charles university', 'czech technical university', 'masaryk university',
            'brno university of technology', 'university of economics prague'
        ],
        'hungary': [
            'eötvös loránd university', 'budapest university of technology',
            'university of szeged', 'university of debrecen', 'corvinus university'
        ],
        'portugal': [
            'university of porto', 'university of lisbon', 'university of coimbra',
            'nova university lisbon', 'university of aveiro', 'university of minho'
        ],
        'greece': [
            'national technical university of athens', 'university of athens',
            'aristotle university of thessaloniki', 'university of crete',
            'university of patras', 'athens university of economics'
        ],
        'turkey': [
            'boğaziçi university', 'middle east technical university', 'istanbul technical university',
            'koç university', 'sabancı university', 'bilkent university', 'hacettepe university',
            'ankara university', 'istanbul university', 'gazi university'
        ],
        'russia': [
            'moscow state university', 'saint petersburg state university',
            'novosibirsk state university', 'moscow institute of physics and technology',
            'higher school of economics', 'bauman moscow state technical university'
        ],
        'japan': [
            'university of tokyo', 'kyoto university', 'osaka university', 'tohoku university',
            'nagoya university', 'kyushu university', 'hokkaido university', 'tokyo institute of technology',
            'waseda university', 'keio university', 'tsukuba university', 'hiroshima university',
            'kobe university', 'yokohama national university', 'chiba university',
            'kanazawa university', 'okayama university', 'kumamoto university'
        ],
        'south korea': [
            'seoul national university', 'kaist', 'postech', 'yonsei university',
            'korea university', 'sungkyunkwan university', 'hanyang university',
            'kyung hee university', 'ewha womans university', 'sogang university'
        ],
        'china': [
            'tsinghua university', 'peking university', 'fudan university', 'shanghai jiao tong university',
            'zhejiang university', 'nanjing university', 'university of science and technology of china',
            'harbin institute of technology', 'xi\'an jiaotong university', 'beihang university',
            'tianjin university', 'dalian university of technology', 'southeast university',
            'huazhong university of science and technology', 'sun yat-sen university',
            'sichuan university', 'central south university', 'jilin university',
            'nankai university', 'beijing institute of technology', 'tongji university',
            'east china normal university', 'beijing normal university', 'renmin university of china',
            'china agricultural university', 'beijing university of posts and telecommunications',
            'zhejiang university of technology', 'south china university of technology'
        ],
        'taiwan': [
            'national taiwan university', 'national tsing hua university', 'national chiao tung university',
            'national cheng kung university', 'national yang ming university', 'national central university',
            'national sun yat-sen university', 'national taiwan normal university'
        ],
        'hong kong': [
            'university of hong kong', 'chinese university of hong kong', 'hong kong university of science and technology',
            'city university of hong kong', 'hong kong polytechnic university', 'baptist university of hong kong',
            'lingnan university', 'education university of hong kong'
        ],
        'singapore': [
            'national university of singapore', 'nanyang technological university',
            'singapore management university', 'singapore university of technology and design'
        ],
        'malaysia': [
            'university of malaya', 'universiti putra malaysia', 'universiti kebangsaan malaysia',
            'universiti sains malaysia', 'universiti teknologi malaysia', 'universiti utara malaysia'
        ],
        'thailand': [
            'chulalongkorn university', 'mahidol university', 'thammasat university',
            'kasetsart university', 'king mongkut\'s university of technology'
        ],
        'indonesia': [
            'university of indonesia', 'institut teknologi bandung', 'gadjah mada university',
            'universitas gadjah mada', 'bogor agricultural university', 'airlangga university',
            'universitas airlangga', 'institut teknologi sepuluh nopember', 'universitas brawijaya'
        ],
        'philippines': [
            'university of the philippines', 'ateneo de manila university', 'de la salle university',
            'university of santo tomas', 'adamson university'
        ],
        'vietnam': [
            'vietnam national university', 'hanoi university of science and technology',
            'ho chi minh city university of technology', 'hue university'
        ],
        'india': [
            'indian institute of science', 'indian institute of technology', 'jawaharlal nehru university',
            'university of delhi', 'university of mumbai', 'university of calcutta',
            'indian statistical institute', 'tata institute of fundamental research',
            'indian institute of science education and research', 'all india institute of medical sciences',
            'banaras hindu university', 'aligarh muslim university', 'jamia millia islamia',
            'jadavpur university', 'anna university', 'university of hyderabad'
        ],
        'iran': [
            'university of tehran', 'sharif university of technology', 'amirkabir university of technology',
            'isfahan university of technology', 'ferdowsi university of mashhad', 'shiraz university',
            'tabriz university', 'yazd university'
        ],
        'israel': [
            'hebrew university of jerusalem', 'tel aviv university', 'technion',
            'weizmann institute of science', 'bar-ilan university', 'university of haifa',
            'ben-gurion university of the negev'
        ],
        'egypt': [
            'cairo university', 'american university in cairo', 'alexandria university',
            'ain shams university', 'assiut university', 'mansoura university'
        ],
        'south africa': [
            'university of cape town', 'university of the witwatersrand', 'stellenbosch university',
            'university of kwazulu-natal', 'university of pretoria', 'rhodes university'
        ],
        'nigeria': [
            'university of ibadan', 'university of nigeria', 'ahmadu bello university',
            'university of lagos', 'obafemi awolowo university'
        ],
        'kenya': [
            'university of nairobi', 'kenyatta university', 'moi university', 'egerton university'
        ],
        'ghana': [
            'university of ghana', 'kwame nkrumah university of science and technology',
            'university of cape coast'
        ],
        'morocco': [
            'mohammed v university', 'hassan ii university', 'cadi ayyad university'
        ],
        'brazil': [
            'university of são paulo', 'university of campinas', 'federal university of rio de janeiro',
            'federal university of minas gerais', 'federal university of rio grande do sul',
            'pontifical catholic university of rio de janeiro', 'federal university of santa catarina',
            'state university of campinas', 'federal university of pernambuco'
        ],
        'argentina': [
            'university of buenos aires', 'national university of córdoba',
            'national university of la plata', 'universidad torcuato di tella'
        ],
        'chile': [
            'university of chile', 'pontifical catholic university of chile',
            'university of santiago', 'universidad de concepción'
        ],
        'colombia': [
            'national university of colombia', 'university of los andes',
            'pontifical javeriana university', 'university of antioquia'
        ],
        'mexico': [
            'national autonomous university of mexico', 'tecnológico de monterrey',
            'instituto politécnico nacional', 'universidad iberoamericana'
        ],
        'peru': [
            'national university of san marcos', 'pontifical catholic university of peru',
            'universidad nacional de ingeniería'
        ],
        'canada': [
            'university of toronto', 'university of british columbia', 'mcgill university',
            'university of alberta', 'university of montreal', 'university of calgary',
            'university of ottawa', 'university of waterloo', 'queen\'s university',
            'university of manitoba', 'university of saskatchewan', 'dalhousie university',
            'university of victoria', 'simon fraser university', 'carleton university',
            'concordia university', 'york university', 'ryerson university', 'university of guelph',
            'mcmaster university'
        ],
        'australia': [
            'university of melbourne', 'university of sydney', 'australian national university',
            'university of queensland', 'university of new south wales', 'monash university',
            'university of western australia', 'university of adelaide', 'macquarie university',
            'university of technology sydney', 'queensland university of technology',
            'deakin university', 'griffith university', 'la trobe university', 'rmit university',
            'unsw sydney', 'unsw', 'university of new south wales sydney'
        ],
        'new zealand': [
            'university of auckland', 'university of otago', 'victoria university of wellington',
            'university of canterbury', 'massey university', 'university of waikato',
            'lincoln university', 'auckland university of technology'
        ],
        'united kingdom': [
            'university of oxford', 'university of cambridge', 'imperial college', 'university college london',
            'london school of economics', 'kings college london', 'university of edinburgh',
            'university of manchester', 'university of bristol', 'university of warwick',
            'university of glasgow', 'university of birmingham', 'university of sheffield',
            'university of nottingham', 'university of southampton', 'university of leeds',
            'university of liverpool', 'university of york', 'university of exeter',
            'university of bath', 'university of durham', 'university of st andrews',
            'loughborough university', 'university of surrey', 'university of leicester',
            'university of reading', 'university of sussex', 'university of east anglia',
            'cardiff university', 'queen mary university of london', 'university of strathclyde'
        ]
    }
    
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
        'canada': 'CA', 'australia': 'AU', 'new zealand': 'NZ', 'united kingdom': 'GB'
    }
    
    # Web address patterns for countries
    web_patterns = {
        'united states': ['.edu', '.us'],
        'germany': ['.de'],
        'italy': ['.it'],
        'spain': ['.es'],
        'france': ['.fr'],
        'netherlands': ['.nl'],
        'belgium': ['.be'],
        'switzerland': ['.ch'],
        'austria': ['.at'],
        'sweden': ['.se'],
        'norway': ['.no'],
        'denmark': ['.dk'],
        'finland': ['.fi'],
        'poland': ['.pl'],
        'czech republic': ['.cz'],
        'hungary': ['.hu'],
        'portugal': ['.pt'],
        'greece': ['.gr'],
        'turkey': ['.tr'],
        'russia': ['.ru'],
        'japan': ['.jp'],
        'south korea': ['.kr'],
        'china': ['.cn'],
        'taiwan': ['.tw'],
        'hong kong': ['.hk'],
        'singapore': ['.sg'],
        'malaysia': ['.my'],
        'thailand': ['.th'],
        'indonesia': ['.id'],
        'philippines': ['.ph'],
        'vietnam': ['.vn'],
        'india': ['.in'],
        'iran': ['.ir'],
        'israel': ['.il'],
        'egypt': ['.eg'],
        'south africa': ['.za'],
        'nigeria': ['.ng'],
        'kenya': ['.ke'],
        'ghana': ['.gh'],
        'morocco': ['.ma'],
        'brazil': ['.br'],
        'argentina': ['.ar'],
        'chile': ['.cl'],
        'colombia': ['.co'],
        'mexico': ['.mx'],
        'peru': ['.pe'],
        'canada': ['.ca'],
        'australia': ['.au'],
        'new zealand': ['.nz'],
        'united kingdom': ['.uk', '.ac.uk']
    }
    
    def infer_country_from_name(name):
        name_lower = name.lower()
        for country, patterns in university_patterns.items():
            for pattern in patterns:
                if pattern in name_lower:
                    return country, country_codes.get(country, '')
        return None, None
    
    def infer_country_from_web(web_address):
        if not web_address:
            return None, None
        
        web_lower = web_address.lower()
        for country, patterns in web_patterns.items():
            for pattern in patterns:
                # More specific matching to avoid false positives
                if pattern == '.co':
                    # Only match .co if it's specifically .edu.co or ends with .co
                    if '.edu.co' in web_lower or web_lower.endswith('.co') or web_lower.endswith('.co/'):
                        return country, country_codes.get(country, '')
                elif web_lower.endswith(pattern) or web_lower.endswith(pattern + '/'):
                    return country, country_codes.get(country, '')
        return None, None
    
    # Process universities
    fixed_count = 0
    for university in universities:
        if university.get('country') in [None, '', 'Unknown']:
            name = university.get('name', '')
            web_address = university.get('web_address', '')
            
            # Try to infer country from name first
            country, country_code = infer_country_from_name(name)
            
            # If not found, try web address
            if not country:
                country, country_code = infer_country_from_web(web_address)
            
            if country:
                university['country'] = country.title()
                university['country_code'] = country_code
                print(f"Fixed: {name} -> {country.title()} ({country_code})")
                fixed_count += 1
            else:
                print(f"Could not determine country for: {name}")
    
    print(f"\nFixed {fixed_count} universities with null/unknown countries")
    
    # Save the updated JSON
    output_file = 'updated_universities_fixed.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(universities, f, indent=2, ensure_ascii=False)
    
    print(f"Updated JSON saved to: {output_file}")

if __name__ == "__main__":
    comprehensive_country_fix()