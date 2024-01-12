import aiohttp
import asyncio
import re
import time
from bs4 import BeautifulSoup
import requests

import leer_articulos

# links = leer_articulos.obtener()

def carrefour(pagina):
    # precio = pagina.find_all("span", class_="valtech-carrefourar-dynamic-weight-price-0-x-container")
    # print(precio)
    if type(pagina) != BeautifulSoup:
        soup = BeautifulSoup(pagina.content, 'html.parser')
    else:
        soup = pagina
    print(type(soup))
    elementos = soup.find_all('span', {'data-specification-name': "pricePerUnit"})
    for i in elementos:
        if i.has_attr("data-specification-value"):
            print(i['data-specification-value'])

def coto(pagina):
    if type(pagina) != BeautifulSoup:
        soup = BeautifulSoup(pagina.content, 'html.parser')
    else:
        soup = pagina
    elemento = soup.find('span', class_="unit")
    elemento.text
    patron = r'\$([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2})'
    coincidencia = re.search(patron, elemento.text)
    print(coincidencia.group(1))

# coto(requests.get("https://www.cotodigital3.com.ar/sitios/cdigi/producto/-coca-cola-zero-15-lt/_/A-00179043-00179043-200"))
# html = requests.get("https://www.carrefour.com.ar/jam-n-crudo-feteado-lario-x-120-grs/p")
# carrefour(html)



async def main():
    inicio = time.time()
    async with aiohttp.ClientSession() as session:
        for ingrediente in links.values():
            for url in ingrediente["links_coto"]:
                ingrediente["html_coto"].append(await fetch(session, url))
            for url in ingrediente["links_dia"]:
                ingrediente["html_dia"].append(await fetch(session, url))
            for url in ingrediente["links_carrefour"]:
                ingrediente["html_carrefour"].append(await fetch(session, url))
                
    for ingrediente in links.values():
        for html in ingrediente["html_coto"]:
            resultados = coto(BeautifulSoup(html.decode('utf-8'), 'html.parser'))
            ingrediente["precios"].append(resultados[0])
            ingrediente["unidades"].append(resultados[1])
        for html in ingrediente["html_dia"]:
            resultados = dia(BeautifulSoup(html.decode('utf-8'), 'html.parser'))
            ingrediente["precios"].append(resultados[0])
            ingrediente["unidades"].append(resultados[1])
        for html in ingrediente["html_carrefour"]:
            resultados = carrefour(BeautifulSoup(html.decode('utf-8'), 'html.parser'))
            ingrediente["precios"].append(resultados[0])
            ingrediente["unidades"].append(resultados[1])        
        ingrediente["precio"] = (sum(ingrediente["precios"])/len(ingrediente["precios"]))
        unidades = promedio_unidades(ingrediente["unidades"])
        print(f"{ingrediente['nombre'].capitalize()}: ${ingrediente['precio']} / {'kg' if unidades == 'kilo' else 'l'}")

    print("Tiempo total: " + str(round(time.time() - inicio, 3)))

# loop = asyncio.get_event_loop()
# pagina = loop.run_until_complete(main())