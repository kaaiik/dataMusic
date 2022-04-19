import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

#---------------------------------------------------------------------------------------------

def get_df(url):
    html = requests.get(url).content
    
    soup = bs(html, 'html.parser')
    
    tabla = soup.find_all('table')[0]
    
    filas = tabla.find_all('tr')
    
    columnas = filas[0].find_all('th')
    cols = [i.text.split('\n')[0] for i in columnas]
    
    filas_def = []

    for i in range(1, len(filas)):
        fila_i = filas[i].find_all('td')
        filas_def.append(fila_i)

    data = []

    for i in range(len(filas_def)):
        aux = []
        for j in range(len(filas_def[i])):
            elem = filas_def[i][j].text
            aux.append(elem)
        data.append(aux)
        
    for i in range(len(data)):
        data[i][2] = data[i][2][:-1]
    
    df = pd.DataFrame(data, columns=cols)
    return df
