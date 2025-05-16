#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup

print("Teste")

def get_dolar_uol():
    """
    Try to scrape UOL’s static HTML for the “Dólar Comercial” heading.
    Fallback to the public JSON API if the static scrape fails.
    """
    url = 'https://economia.uol.com.br/cotacoes/cambio/'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # UOL shows in static HTML: “Dólar Comercial -0,19% R$ 5,668” :contentReference[oaicite:0]{index=0}
    heading = soup.find('h3', string=re.compile(r'Dólar Comercial'))
    if heading:
        m = re.search(r'R\$[\s]*([\d.,]+)', heading.text)
        if m:
            return m.group(1)

    # Fallback: use AwesomeAPI (same data UOL consumes under the hood)
    api = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    data = requests.get(api).json()
    return data['USDBRL']['bid']

def get_dolar_wise():
    """
    Scrape Wise’s converter page for the “1 USD = … BRL” line.
    """
    url = 'https://wise.com/br/currency-converter/dolar-hoje'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Wise page includes “### 1 USD = 5.66510 BRL” :contentReference[oaicite:1]{index=1}
    heading = soup.find('h3', string=re.compile(r'1\s*USD\s*='))
    if heading:
        m = re.search(r'1\s*USD\s*=\s*([\d.,]+)', heading.text)
        if m:
            return m.group(1)
    raise RuntimeError("Could not parse Wise rate")

def get_dolar_valor():
    """
    Scrape Valor Data’s header ticker list for “Dólar comercial R$ …” string.
    """
    url = 'https://valor.globo.com/valor-data/'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Valor Data shows “Dólar comercial R$ 5,6685” :contentReference[oaicite:2]{index=2}
    text = soup.find(string=re.compile(r'Dólar comercial R\$ [\d.,]+'))
    if text:
        m = re.search(r'R\$[\s]*([\d.,]+)', text)
        if m:
            return m.group(1)
    raise RuntimeError("Could not parse Valor Data rate")

if __name__ == '__main__':
    print('UOL Economia (Commercial USD):', get_dolar_uol())
    print('Wise (1 USD → BRL):', get_dolar_wise())
    print('Valor Data (Commercial USD):', get_dolar_valor())
