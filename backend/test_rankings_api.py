import requests
import json

try:
    response = requests.get('http://localhost:8000/universities')
    print('API Status:', response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        print('Response type:', type(data))
        print('Total items returned:', len(data) if isinstance(data, list) else 'Not a list')
        
        if isinstance(data, list) and len(data) > 0:
            print('First item type:', type(data[0]))
            print('First item sample:', data[0] if isinstance(data[0], dict) else str(data[0])[:100])
            
            # Get top 5 universities by ranking if data is properly formatted
            if isinstance(data[0], dict):
                top_unis = sorted([u for u in data if u.get('ranking') is not None], key=lambda x: x['ranking'])[:5]
                print('\nTop 5 universities from API:')
                for u in top_unis:
                    print(f"{u['ranking']}: {u['name']} ({u['country']})")
        else:
            print('Data structure:', data)
    else:
        print('API Error:', response.text)
        
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()