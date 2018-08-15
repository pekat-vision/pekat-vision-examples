import requests


with open('cat.jpg', 'rb') as data:
    response = requests.post(
        url='http://127.0.0.1:8000/analyze_image',
        data=data.read(),
        headers={'Content-Type': 'application/octet-stream'}
    )
    print(response.json())



