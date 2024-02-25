import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt

def obtener_index(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # Espera unos segundos para asegurar que la página se cargue completamente

    # Encuentra el elemento que contiene la cantidad de resultados indexados
    index_element = driver.find_element(By.XPATH, '//*[@id="result-stats"]')
    
    # Obtén el texto que contiene el número de resultados
    index_text = index_element.text
    
    # Extrae el número de resultados usando expresiones regulares
    import re
    match = re.search(r"Cerca de ([\d,]+) resultados", index_text)
    if match:
        index = match.group(1)
    else:
        index = None
    
    driver.quit()
    
    # Eliminar los caracteres no numéricos y convertir a entero
    if index:
        index = int(index.replace(',', ''))
    
    return index


def main():
    st.title('Análisis de Páginas Indexadas')

    urls_str = st.text_input("Ingrese las URLs separadas por coma (por ejemplo, ejemplo.com, prueba.com): ")

    if st.button("Obtener URLs Indexadas"):
        urls = [url.strip() for url in urls_str.split(',')]
        
        indexes = {}
        
        for url in urls:
            search_url = f'https://www.google.com/search?q=site%3A{url}&oq=site%3A{url}&aqs=chrome..69i57j69i58.6029j0j1&sourceid=chrome&ie=UTF-8'
            index = obtener_index(search_url)
            indexes[url] = index
            time.sleep(1)

        df = pd.DataFrame.from_dict(indexes, orient='index', columns=['Páginas indexadas'])
        df.sort_values(by='Páginas indexadas', ascending=False, inplace=True)

        # Mostrar la tabla de datos
        st.write(df)

        # Crear un gráfico de torta
        explode = [0.1] * len(df)  # Separación entre las porciones
        colors = plt.cm.Set3(range(len(df)))  # Paleta de colores
        fig, ax = plt.subplots()
        ax.pie(df['Páginas indexadas'], labels=df.index, autopct='%1.1f%%', explode=explode, colors=colors, shadow=True, startangle=90)
        ax.set_title('Páginas Indexadas')
        ax.axis('equal')  # Asegura una forma circular
        st.pyplot(fig)

        st.markdown("También puedes seguirme en [LinkedIn](https://www.linkedin.com/in/tomasezequiel)")

if __name__ == "__main__":
    main()
