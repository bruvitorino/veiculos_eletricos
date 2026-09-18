import time     
import re
import os
import unicodedata
from urllib.parse import unquote, urlparse

import requests

from .coletar_links_senatran import HEADERS, coletar_links_ano


PASTA_RAW = "data/raw/senatran/frota_combustivel"

MESES = {
    "jan": "01",
    "janeiro": "01",
    "janeito": "01",
    "fev": "02",
    "fevereiro": "02",
    "mar": "03",
    "marco": "03",
    "maro": "03",
    "abr": "04",
    "abril": "04",
    "mai": "05",
    "maio": "05",
    "jun": "06",
    "junho": "06",
    "jul": "07",
    "julho": "07",
    "ago": "08",
    "agosto": "08",
    "set": "09",
    "setembro": "09",
    "out": "10",
    "outubro": "10",
    "nov": "11",
    "novembro": "11",
    "dez": "12",
    "dezembro": "12",
}

def normalizar_texto(texto):
    texto = texto.lower()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def identificar_mes(nome_arquivo):
    nome_normalizado = normalizar_texto(nome_arquivo)

    partes_nome = re.split(
        r"[^a-z0-9]+",
        nome_normalizado
    )

    for parte in partes_nome:
        if parte in MESES:
            return MESES[parte]

    return None 


def baixar_arquivo(url, ano):
    nome_arquivo = unquote(
        os.path.basename(urlparse(url).path)
    )

    mes = identificar_mes(nome_arquivo)

    if mes is None:
        print(
            f"Não foi possível identificar o mês: "
            f"{nome_arquivo}"
        )
        return

    pasta_destino = os.path.join(
        PASTA_RAW,
        str(ano),
        mes
    )

    os.makedirs(
        pasta_destino,
        exist_ok=True
    )

    caminho_destino = os.path.join(
        pasta_destino,
        nome_arquivo
    )

    if os.path.exists(caminho_destino):
        print(
            f"Já existe: {ano}/{mes}/{nome_arquivo}"
        )
        return

    resposta = requests.get(
        url,
        headers=HEADERS,
        timeout=60
    )

    resposta.raise_for_status()

    with open(caminho_destino, "wb") as arquivo:
        arquivo.write(resposta.content)

    print(
        f"Baixado: {ano}/{mes}/{nome_arquivo}"
    )


def main():

    for ano in range(2017, 2027):

        print(f"\n{'=' * 60}")
        print(f"Processando ano: {ano}")
        print(f"{'=' * 60}")

        links = coletar_links_ano(ano)

        print(
            f"Arquivos encontrados para {ano}: "
            f"{len(links)}\n"
        )

        for url in links:

            try:
                baixar_arquivo(url, ano)

                time.sleep(0.5)

            except requests.RequestException as erro:
                print(
                    f"Erro ao baixar arquivo: {erro}"
                )

if __name__ == "__main__":
    main()