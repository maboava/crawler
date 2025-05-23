import requests
from bs4 import BeautifulSoup
from pathlib import Path
import csv
from datetime import datetime, timedelta


def validar_csv(caminho_arquivo: str = "resultados.csv"):
    """
    Garante que o arquivo CSV exista antes de iniciar a coleta.
    - Se o arquivo não existir, cria um arquivo vazio.
    """
    caminho = Path(caminho_arquivo)
    caminho.touch(exist_ok=True)


def grava_csv(
    data_hora: str,
    identificador: str,
    url: str,
    valor: float,
    caminho_arquivo: str = "resultados.csv"
):
    """
    Abre ou cria o CSV e adiciona uma linha com os dados de cotação.

    Parâmetros:
    - data_hora: timestamp da coleta (formato dd/mm/AAAA HH:MM:SS)
    - identificador: nome da fonte (ex.: 'Dólar Hoje')
    - url: endereço da fonte consultada
    - valor: cotação extraída (float)
    """
    caminho = Path(caminho_arquivo)
    primeira_escrita = caminho.stat().st_size == 0

    with caminho.open("a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        if primeira_escrita:
            escritor.writerow(["data_hora", "id", "url", "valor"]);
        escritor.writerow([data_hora, identificador, url, valor])


def sites():
    """
    Percorre cada fonte de cotação, faz requisição HTTP e extrai o valor.
    - Se ocorrer erro na requisição ou extração, ignora a fonte.
    """
    fontes = [
        {"id": "Dólar Hoje", "url": "https://www.dolarhoje.com/", "referencia": "nacional"},
        {"id": "Wise",      "url": "https://wise.com/br/currency-converter/dolar-hoje", "referencia": "target-input"},
        {"id": "Melhor Câmbio", "url": "https://www.melhorcambio.com/dolar-hoje", "referencia": "comercial"}
    ]

    for fonte in fontes:
        try:
            resposta = requests.get(
                fonte['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10
            )
            resposta.raise_for_status()
        except requests.RequestException:
            continue

        try:
            sopa = BeautifulSoup(resposta.text, 'html.parser')
            bruto = sopa.select_one(f"input#{fonte['referencia']}")["value"]
            valor = float(bruto.replace(',', '.'))
        except Exception:
            continue

        data_hora = (datetime.now() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        grava_csv(data_hora, fonte['id'], fonte['url'], valor)


if __name__ == "__main__":
    validar_csv()
    sites()
    print("Coleta concluída.")
    