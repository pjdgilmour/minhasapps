import os
import shutil
from datetime import datetime
import tkinter as tk

# Função para organizar arquivos
def organizar_arquivos():
    # Exibindo mensagem de organização
    lbl_status.config(text="Organizando arquivos...")
    root.update_idletasks()
    
    # Definindo pastas
    pasta_origem = os.getcwd()  # Pasta de onde o script é executado
    pasta_recentes = os.path.join(pasta_origem, "recentes")
    pasta_verificar = os.path.join(pasta_origem, "verificar")
    pasta_apagar = os.path.join(pasta_origem, "apagar")

    # Criando pastas caso não existam
    for pasta in [pasta_recentes, pasta_verificar, pasta_apagar]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    # Definindo limite de dias para cada pasta
    limite_recentes = 30
    limite_verificar = 90

    # Obter data de hoje
    data_hoje = datetime.today()

    # Iterando pelos arquivos na pasta de origem
    for arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        
        # Verificando se é um arquivo
        if os.path.isfile(caminho_arquivo):
            # Obtendo data de criação e modificação do arquivo
            data_criacao = datetime.fromtimestamp(os.path.getctime(caminho_arquivo))
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))

            # Calculando diferença em dias entre data de hoje e datas de criação e modificação
            diferenca_criacao = (data_hoje - data_criacao).days
            diferenca_modificacao = (data_hoje - data_modificacao).days

            # Definindo pasta de destino de acordo com a menor diferença em dias
            if diferenca_criacao <= limite_recentes or diferenca_modificacao <= limite_recentes:
                pasta_destino = pasta_recentes
            elif diferenca_criacao <= limite_verificar or diferenca_modificacao <= limite_verificar:
                pasta_destino = pasta_verificar
            else:
                pasta_destino = pasta_apagar

            # Movendo o arquivo para a pasta de destino
            shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))

    # Mensagem de sucesso
    lbl_status.config(text="Organização de arquivos finalizada com sucesso!")

    # Fechar o programa após 5 segundos
    root.after(5000, root.quit)

# Criando a interface gráfica
root = tk.Tk()
root.title("Organizador de Arquivos")

# Label de status
lbl_status = tk.Label(root, text="")
lbl_status.pack(pady=10)

# Botão para iniciar a organização
btn_organizar = tk.Button(root, text="Organizar Arquivos", command=organizar_arquivos)
btn_organizar.pack(pady=10)

# Iniciando o loop da interface gráfica
root.mainloop()