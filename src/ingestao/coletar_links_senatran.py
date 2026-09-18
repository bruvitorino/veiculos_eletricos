import unicodedata
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL_BASE = (
    "https://www.gov.br/transportes/pt-br/assuntos/transito/"
    "conteudo-Senatran/frota-de-veiculos-{}"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/146.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


def normalizar_texto(texto):
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def coletar_links_ano(ano):
    url_pagina = URL_BASE.format(ano)

    resposta = requests.get(
        url_pagina,
        headers=HEADERS,
        timeout=30
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    links_combustivel = []

    for link in soup.find_all("a", href=True):
        texto_link = normalizar_texto(
            link.get_text(" ", strip=True)
        )

        if "uf municipio" in texto_link and "combustivel" in texto_link:
            url_completa = urljoin(
                url_pagina,
                link["href"]
            )

            links_combustivel.append(url_completa)

    return list(dict.fromkeys(links_combustivel))

def main():
    todos_links = {}

    for ano in range(2017, 2027):
        try:
            links = coletar_links_ano(ano)

            todos_links[ano] = links

            print(
                f"{ano}: {len(links)} arquivos encontrados"
            )

        except requests.RequestException as erro:
            print(
                f"{ano}: erro ao acessar página - {erro}"
            )

    total = sum(
        len(links)
        for links in todos_links.values()
    )

    print(f"\nTotal encontrado: {total}")


if __name__ == "__main__":
    main()