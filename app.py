import requests
from bs4 import BeautifulSoup

valores = []

def sites():
    urls = [
        {"url": "https://www.dolarhoje.com/", "reference": "nacional"},
        {"url": "https://wise.com/br/currency-converter/dolar-hoje", "reference": "target-input"},
        {"url": "https://www.melhorcambio.com/dolar-hoje", "reference": "comercial"},
    ]

    for n in urls:
        resp = requests.get(n["url"], headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        soup = BeautifulSoup(resp.text, "html.parser")
        reference = n["reference"]
        dolar_compra = soup.select_one(f"input#{reference}")["value"]

        dolar_compra = float(str((dolar_compra.replace(",","."))))
        valores.append(dolar_compra)

sites()       
print(valores)