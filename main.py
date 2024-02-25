import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import matplotlib.pyplot as plt

def obtener_index(url):
    service = Service('/chromedriver')  # Update this with the path to your Chromedriver executable
    service.start()
    driver = webdriver.Chrome(service=service)
    
    driver.get(url)
    index = driver.find_element(By.XPATH, '//*[@id="result-stats"]').text
    try:
        index = index.split('Cerca de ')[1].split(' resultados')[0]
        index = index.replace('.', '').replace(',', '').replace(' ', '')
        return int(index)
    except IndexError:
        print("Error: Unable to extract index information from the page.")
        return None
    finally:
        driver.quit()


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
