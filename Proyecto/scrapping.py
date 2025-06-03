import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# URL base ordenada por fecha (más recientes)
base_url = "https://www.remax.com.ar/listings/buy?page={}&pageSize=24&sort=-createdAt&in:operationId=1&in:eStageId=0,1,2,3,4&locations=in:::458@%3Cb%3ESanta%3C%2Fb%3E%20%3Cb%3EFe%3C%2Fb%3E%20Capital::::&landingPath=&filterCount=0&viewMode=listViewMode"

# Número de páginas a recorrer (ajustable)
total_paginas = 100

data = []

for pagina in range(total_paginas):
    print(f"Procesando página {pagina + 1}")
    url = base_url.format(pagina)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.select('.card-remax__container')

    for card in cards:
        nombre = card.select_one('.card__description')
        precio = card.select_one('.card__price')
        direccion = card.select_one('.card__address')
        m2 = card.select_one('.feature--m2total span')
        ambientes = card.select_one('.feature--ambientes span')
        baños = card.select_one('.feature--bathroom span')

        data.append({
            "Nombre": nombre.get_text(strip=True) if nombre else "",
            "Precio USD": precio.get_text(strip=True).replace("USD", "").strip() if precio else "",
            "Dirección": direccion.get_text(strip=True) if direccion else "",
            "M2 Totales": m2.get_text(strip=True).replace(",", ".") if m2 else "",
            "Ambientes": ambientes.get_text(strip=True) if ambientes else "",
            "Baños": baños.get_text(strip=True) if baños else ""
        })

    time.sleep(1.5)  # Espera entre requests

df = pd.DataFrame(data)
df.to_csv("propiedades_bruto.csv", index=False, encoding='utf-8')