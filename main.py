import os
import time
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright



def download_leyes_promulgadas():
    """Descarga la pagina web de la camara de chile donde se encuentra todas las leyes del pais"""

    url = "https://www.camara.cl/legislacion/proyectosdeley/leyes_promulgadas.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open("./web/leyes_promulgadas.html", "w", encoding="utf-8") as file:
            file.write(response.text)
        print("Página descargada con éxito.")
    else:
        print(f"Error {response.status_code}: No se pudo descargar la página.")

def read_pages_leyes_promulgadas():
    """Lee la pagina web descarga y atravez de la libreria BeautifulSoup y expresiones regulares
    extrae la informacion correspondiente a la tabla de las leyes promulgadas"""

    if os.path.exists("./web/leyes_promulgadas.html"):

        with open("./web/leyes_promulgadas.html", "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        tabla = soup.find("table", class_="tabla")
        datos = []

        regex_numero_ley = re.compile(r"\d+\.\d+")

        for fila in tabla.find_all("tr")[1:]:
            columnas = fila.find_all("td")

            if len(columnas) >= 6:
                numero_proyecto = columnas[0].text.strip()
                fecha_ingreso = columnas[1].text.strip()
                iniciativa = columnas[2].text.strip()
                proyecto_suma = columnas[3].text.strip()
                numero_ley = columnas[4].text.strip()
                fecha_publicacion = columnas[5].text.strip()

                numero_ley_match = regex_numero_ley.search(numero_ley)
                if numero_ley_match:
                    numero_ley = int(numero_ley_match.group().replace(".", ""))
                else:
                    numero_ley = None

                datos.append([numero_proyecto, fecha_ingreso, iniciativa, proyecto_suma, numero_ley, fecha_publicacion])

        df = pd.DataFrame(datos, columns=[
            "numero_proyecto", "fecha_ingreso", "iniciativa", "proyecto_suma", "numero_ley", "fecha_publicacion"
        ])

        # Se elimina las filas que no tenga un numero de ley asociada
        df = df.dropna(subset=['numero_ley'])

        df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"], format="%d-%m-%Y", errors="coerce")
        df["fecha_publicacion"] = pd.to_datetime(df["fecha_publicacion"], format="%d-%m-%Y", errors="coerce")
        df['numero_ley'] = df['numero_ley'].astype(int)

        print("DataFrame leyes_promulgadas")
        df.to_csv("./data/leyes_promulgadas.csv", index=False, encoding="utf-8")

        # Se filtra el DataFrame por las leyes iguales o mayores a 2023
        df_filtrado = df[df["fecha_ingreso"].dt.year >= 2023]
        df_filtrado.to_csv("./data/leyes_promulgadas_2023_to_2025.csv", index=False, encoding="utf-8")
        lista_leyes_actuales = list(df_filtrado["numero_ley"])
        return lista_leyes_actuales
    else:
        return None


async def scrape_page(numero_ley):
    """Hace un web scraping a la pagina de la biblioteca del congreso nacional de chile
    utilizando la libreria playwright, va variando el idLey para consultar los temas
    principales y el resumen de la ley
    """

    url = f"https://www.bcn.cl/leychile/navegar?idLey={numero_ley}"
    print(url)

    async with async_playwright() as p:
        # Se inicia el navegador
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        try:
            # Esperar a que el botón con role="button" esté disponible se hace click
            await page.wait_for_selector("span[role='button']", state="visible", timeout=5000)
            await page.click("span[role='button']")

            await page.wait_for_selector("span[itemprop='accessibilitySummary']", state="visible", timeout=5000)
        except Exception as e:
            print(f"Error al hacer clic o cargar el contenido: {e}")

        finally:
            html_content = await page.content()
            await browser.close()

    return html_content


def extraer_materias_resumen_ley(numero_ley, html_result):
    soup = BeautifulSoup(html_result, "html.parser")
    div_datos = soup.find("div", class_="datos")
    keywords_materias = div_datos.find_all("span", itemprop="keywords")
    materias = ""
    for span in keywords_materias:
        materias += span.text.strip()

    accessibility_summary = div_datos.find_all("span", itemprop="accessibilitySummary")
    summary_span = accessibility_summary[0]

    spans = summary_span.find_all("span")
    resumen_ley = spans[0].text.strip()

    return [numero_ley, materias, resumen_ley]


if __name__ == "__main__":

    download_leyes_promulgadas()
    lista_leyes_actuales = read_pages_leyes_promulgadas()

    #lista_leyes_actuales = lista_leyes_actuales[:5] # Decomentar para pruebas

    list_resumen = []

    if lista_leyes_actuales:
        for ley in lista_leyes_actuales:
            try:
                html_result = asyncio.run(scrape_page(ley))
                time.sleep(2)
                list_data = extraer_materias_resumen_ley(ley, html_result)
                list_resumen.append(list_data)
            except:
                pass

    df_resumen_ley = pd.DataFrame(list_resumen, columns=['numero_ley', 'materias', 'resumen'])
    df_resumen_ley.to_csv("./data/leyes_temas_principales_2023_to_2025.csv", index=False, encoding="utf-8")
    print("Execucion terminada")


