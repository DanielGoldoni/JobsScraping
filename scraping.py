from googlesearch import search  # Instale com: pip install googlesearch-python
import requests
from bs4 import BeautifulSoup

# Aqui você seta a vaga que você quer
vaga_desejada = "desenvolvedor"
# Query com o google Dork, recomendo usar nesse formato.
query = "inurl:vagas intext:", vaga_desejada

urls = list(search(query))
# Itera sobre as URLs encontradas para conseguir as vagas com mais precisão (possibilidade para novas filtragens)
for url in urls:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Personalizavel
            vagas = soup.find_all(string=lambda text: "rio de janeiro")
            # if vagas:
            #     print(f"\nVagas encontradas em {url}:")
        else:
            print("Erro na url: ", url)
    except Exception as e:
        print("Erro: ", e)
