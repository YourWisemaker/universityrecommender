import requests
import json

try:
    response = requests.get('http://localhost:8000/universities')
    print('Status:', response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        if 'universities' in data and data['universities']:
            first_uni = data['universities'][0]
            print('First university keys:', list(first_uni.keys()))
            print('\nSample data:')
            print('Name:', first_uni.get('name'))
            print('Program Name:', first_uni.get('programName'))
            print('Admission Rate:', first_uni.get('admission_rate'))
            print('Notable Faculty:', first_uni.get('notable_faculty', '')[:100] + '...' if first_uni.get('notable_faculty') else 'None')
            print('Program Strengths:', first_uni.get('program_strengths', '')[:100] + '...' if first_uni.get('program_strengths') else 'None')
        else:
            print('No universities data found')
    else:
        print('Error response:', response.text)
        
except Exception as e:
    print('Error:', e)