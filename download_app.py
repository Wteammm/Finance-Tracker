import requests
from requests.auth import HTTPBasicAuth

# PythonAnywhere credentials
username = 'wtea'
# We'll need to use an API token or session cookies

# Try direct download URL
url = 'https://www.pythonanywhere.com/user/wtea/files/home/wtea/Finance_Tracker/app.py?download'

# First, let's try without auth (might work if already logged in via browser)
response = requests.get(url)

if response.status_code == 200:
    with open('app_downloaded.py', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Success! Downloaded {len(response.text)} characters")
    print(f"Lines: {len(response.text.splitlines())}")
else:
    print(f"Failed with status code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
