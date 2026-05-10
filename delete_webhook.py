import requests

TOKEN = "8791314159:AAEkTRKl6ki13fR1yEkeNzRn4gxMM2neKW0"

url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
response = requests.get(url)
print(response.json())