import requests

response = requests.get('http://localhost:8000/api/winners', params={'country':'Australia'})
print(response.json())

