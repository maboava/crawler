import requests
from bs4 import BeautifulSoup

url = "https://www.dolarhoje.com/"
resp = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
soup = BeautifulSoup(resp.text, "html.parser")

dolar_compra = soup.select_one("input#nacional")["value"]

print("Dólar COMPRA:", dolar_compra)

