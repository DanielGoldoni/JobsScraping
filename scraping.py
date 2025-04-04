import tkinter as tk
from tkinter import messagebox
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import webbrowser

# Sites de vaga
SITES_INDESEJADOS_PADRAO = ["linkedin", "indeed", "glassdoor", "infojobs", "catho", "empregos", "jooble"]    

# Cabeçalhos para requisição HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def buscar_vagas():
    """Realiza a busca de vagas com base nos critérios do usuário."""

    vagas_texto = vaga_entry.get()
    localizacao = localizacao_entry.get()
    urls_indesejadas_texto = urls_indesejadas_entry.get()
    excluir_sites_vagas = excluir_var.get() 


    if not vagas_texto or not localizacao:
        messagebox.showwarning("Aviso", "Preencha os campos de vaga e localização!")
        return

    # Processa os inputs
    vagas_desejadas = [vaga.strip() for vaga in vagas_texto.split(",")]
    urls_indesejadas = [url.strip() for url in urls_indesejadas_texto.split(",") if url]


    # Se o usuário quiser excluir sites de vagas, adiciona a lista padrão
    if excluir_sites_vagas:
        urls_indesejadas.extend(SITES_INDESEJADOS_PADRAO)

    try:
        urls_encontradas = set()
        
        for vaga in vagas_desejadas:
            query = f"inurl:vagas intext:{vaga} {localizacao}"
            urls = set(search(query)) #Pode colocar um num_results=num para evitar erro 429
            urls_encontradas.update(urls)      
        results_list.delete(0, tk.END)  # Limpa a lista
        
        for url in urls_encontradas:
            if any(site in url for site in urls_indesejadas):
                continue 
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            except requests.RequestException:
                continue  # Pula URLs com erro

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Busca por palavras-chave no texto da página
            junior = soup.find_all(string=lambda text:"júnior")
            if junior:
                    webbrowser.open(url)
                    results_list.insert(tk.END, url)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar vagas: {e}")

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

tk.Label(root, text="Sites indesejados adicionais (separados por vírgula):").pack()
urls_indesejadas_entry = tk.Entry(root, width=50)
urls_indesejadas_entry.pack()


excluir_var = tk.BooleanVar()
excluir_checkbox = tk.Checkbutton(root, text="Excluir sites de vagas conhecidos (LinkedIn, Indeed, etc.)", variable=excluir_var)
excluir_checkbox.pack()

buscar_btn = tk.Button(root, text="Buscar Vagas", command=buscar_vagas)
buscar_btn.pack(pady=10)

results_list = tk.Listbox(root, width=70, height=10)
results_list.pack()

root.mainloop()
