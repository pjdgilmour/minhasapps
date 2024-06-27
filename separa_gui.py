import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def selecionar_pasta():
    # Abrir diálogo de seleção de pasta
    pasta_origem = filedialog.askdirectory()

    # Atualizar entrada de texto com a pasta selecionada
    pasta_origem_entry.delete(0, tk.END)
    pasta_origem_entry.insert(0, pasta_origem)

def separar_imagens():
    # Obter pasta de origem
    pasta_origem = pasta_origem_entry.get()

    # Validar pasta de origem
    if not os.path.isdir(pasta_origem):
        tk.messagebox.showerror("Erro", "Pasta de origem inválida!")
        return

    # Criar subdiretórios
    os.makedirs(os.path.join(pasta_origem, "retrato"), exist_ok=True)
    os.makedirs(os.path.join(pasta_origem, "paisagem"), exist_ok=True)

    # Contar imagens
    numero_imagens = len(os.listdir(pasta_origem))

    # Percorrer arquivos na pasta de origem
    for arquivo in os.listdir(pasta_origem):
        # Ignorar arquivos que não são imagens
        if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Abrir imagem
        imagem = Image.open(os.path.join(pasta_origem, arquivo))

        # Obter largura e altura
        largura, altura = imagem.size

        # Determinar orientação
        if largura > altura:
            orientacao = "paisagem"
        else:
            orientacao = "retrato"

        # Mover imagem para o subdiretório correto
        os.rename(os.path.join(pasta_origem, arquivo),
                  os.path.join(pasta_origem, orientacao, arquivo))

    # Exibir mensagem de sucesso
    tk.messagebox.showinfo("Sucesso", f"{numero_imagens} imagens separadas com sucesso!")

def sair():
    janela.destroy()

# Criar janela
janela = tk.Tk()
janela.title("Separador de Imagens")

# Criar widgets
pasta_origem_label = tk.Label(text="Pasta de Origem:")
pasta_origem_entry = tk.Entry()
selecionar_pasta_button = tk.Button(text="Selecionar Pasta", command=selecionar_pasta)
separar_imagens_button = tk.Button(text="Separar Imagens", command=separar_imagens)
sair_button = tk.Button(text="Sair", command=sair)

# Organizar widgets
pasta_origem_label.pack()
pasta_origem_entry.pack()
selecionar_pasta_button.pack()
separar_imagens_button.pack()
sair_button.pack()

# Iniciar loop da janela
janela.mainloop()
