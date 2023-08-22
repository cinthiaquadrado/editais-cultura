import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from google.colab import files

URL = "https://prosas.com.br/apps/editais"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')

editais = soup.find_all('p', class_='titulo_apps')
prazos = soup.find_all('p', class_='prazo')

termos = ["arte", "artístico", "cultura", "música"]
data_limite = datetime(2023, 8, 22)  # Defina sua data limite aqui

editais_data = []

for edital, prazo in zip(editais, prazos):
    nome = edital.text.strip()
    link = edital.a['href']
    data_str = prazo.text.strip()

    try:
        data = datetime.strptime(data_str.split(' ')[-1], '%d/%m/%y')

        if any(termo in nome.lower() for termo in termos) and data > data_limite:
            editais_data.append({"Nome": nome, "Link": link, "Prazo": data_str})
    except ValueError:
        pass

# Criar um DataFrame usando pandas
df = pd.DataFrame(editais_data)

# Dividir o DataFrame em específicos e contínuos
editais_especificos = df[~df['Prazo'].str.lower().str.contains("contínuas")]
editais_continuos = df[df['Prazo'].str.lower().str.contains("contínuas")]

# Escrever para um arquivo Excel
output_path = "editais.xlsx"
with pd.ExcelWriter(output_path) as writer:
    editais_especificos.to_excel(writer, sheet_name='Específicos', index=False)
    editais_continuos.to_excel(writer, sheet_name='Contínuos', index=False)

print(f"As listas foram exportadas para '{output_path}'.")

files.download('editais.xlsx')

