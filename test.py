import requests

url = "http://127.0.0.1:5000/process_pdfs"
data = {"folder_path": "./pdf"}
response = requests.post(url, json=data)
print(response.json())