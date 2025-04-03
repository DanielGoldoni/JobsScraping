from googlesearch import search
import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import webbrowser

def buscar_vagas():
    # Query com o google Dork, recomendo usar nesse formato.
    vagas_texto = vaga_entry.get()
    localizacao = localizacao_entry.get()
    urls_indesejadas_texto = urls_indesejadas_entry.get()

    if not vagas_texto or not localizacao:
        messagebox.showwarning("Aviso", "Preencha os campos de vaga e localização!")
        return
    
    # Listas preenchidas ou não pelo usuário
    vagas_desejadas = [vaga.strip() for vaga in vagas_texto.split(",")]
    urls_indesejadas = [url.strip() for url in urls_indesejadas_texto.split(",")]
    try:
        urls_encontradas = set()
        for vaga in vagas_desejadas:
            query = f"inurl:vagas intext:{vaga} {localizacao}"
            urls = search(query) 
            urls_encontradas.update(urls) # Evita as URLs duplicadas
        for url in urls_encontradas:
            if any(site in url for site in urls_indesejadas):
                continue         
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, "html.parser")
        junior = soup.find_all(string=lambda text:"júnior")
        if junior:
            finded = soup.find_all(string=lambda text: text and ("python" or "c#" or ".net"))
            if finded:
                webbrowser.open(url)
                results_list.insert(tk.END, url)
    except Exception as e:
        print("Erro: ", e)
        
# Interface gráfica
root = tk.Tk()
root.title("Buscador de Vagas")
root.geometry("500x500")

tk.Label(root, text="Cargos desejados (separados por vírgula):").pack()
vaga_entry = tk.Entry(root, width=50)
vaga_entry.pack()

tk.Label(root, text="Localização:").pack()
localizacao_entry = tk.Entry(root, width=50)
localizacao_entry.pack()

tk.Label(root, text="Sites indesejados (separados por vírgula):").pack()
urls_indesejadas_entry = tk.Entry(root, width=50)
urls_indesejadas_entry.pack()

buscar_btn = tk.Button(root, text="Buscar Vagas", command=buscar_vagas)
buscar_btn.pack(pady=10)

results_list = tk.Listbox(root, width=70, height=10)
results_list.pack()

root.mainloop()
