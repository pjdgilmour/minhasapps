import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import tempfile

def parse_window_maker_menu(content):
    menu_stack = []
    current_menu = None
    menus = {}

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.endswith('MENU'):
            title = line.split('"')[1]
            if current_menu is not None:
                menu_stack.append(current_menu)
            current_menu = {'title': title, 'items': []}
        elif line.endswith('END'):
            if menu_stack:
                parent_menu = menu_stack.pop()
                parent_menu['items'].append(current_menu)
                current_menu = parent_menu
            else:
                menus[current_menu['title']] = current_menu
                current_menu = None
        elif line.startswith('"') and 'EXEC' in line:
            parts = line.split('EXEC')
            title = parts[0].split('"')[1].strip()
            command = parts[1].strip()
            current_menu['items'].append({'title': title, 'command': command})

    return menus

def generate_emwm_menu(menus):
    def generate_menu_text(menu, indent=1):
        ind = '\t' * indent
        text = f"{ind}&{menu['title']}\n{ind}{{\n"
        for item in menu['items']:
            if 'command' in item:
                text += f"{ind}\t&{item['title']}: {item['command']}\n"
            else:
                text += generate_menu_text(item, indent + 1)
        text += f"{ind}}}\n"
        return text

    emwm_text = ""
    for menu in menus.values():
        emwm_text += generate_menu_text(menu)

    return emwm_text

def generate_toolboxrc():
    try:
        # Gerar o arquivo de entrada usando xdg_menu
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, 'entrada.tmp')

        # Executar o comando xdg_menu shell e redirecionar a saída para o arquivo temporário
        command = ['xdg_menu', 'shell']
        with open(temp_file, 'w', encoding='utf-8') as file:
            subprocess.run(command, stdout=file, stderr=subprocess.PIPE, check=True)

        # Renomear o arquivo temporário para entrada.txt
        input_file = os.path.join(temp_dir, 'entrada.txt')
        os.rename(temp_file, input_file)

        # Verificar se o arquivo de entrada foi gerado corretamente
        if not os.path.exists(input_file):
            messagebox.showerror("Erro", "Falha ao gerar o arquivo de entrada.")
            return

        # Ler o conteúdo do arquivo de entrada
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parsear o menu do Window Maker
        menus = parse_window_maker_menu(content)

        # Gerar o conteúdo do arquivo ~/.toolboxrc
        home_directory = os.path.expanduser("~")
        toolboxrc_path = os.path.join(home_directory, ".toolboxrc")
        toolboxrc_content = generate_emwm_menu(menus)

        # Escrever o arquivo ~/.toolboxrc
        with open(toolboxrc_path, 'w', encoding='utf-8') as file:
            file.write(toolboxrc_content)

        messagebox.showinfo("Conversão Completa", "Arquivo ~/.toolboxrc gerado com sucesso!")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro ao executar xdg_menu", f"Ocorreu um erro ao executar xdg_menu: {e.stderr.decode('utf-8')}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante a geração do arquivo ~/.toolboxrc: {str(e)}")

    finally:
        # Remover o arquivo temporário se ainda existir
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Interface Gráfica
root = tk.Tk()
root.title("Automatizador de Conversão para ~/.toolboxrc")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill=tk.BOTH)

label = tk.Label(frame, text="Clique no botão para gerar o arquivo ~/.toolboxrc automaticamente", font=("Helvetica", 16))
label.pack(pady=10)

button = tk.Button(frame, text="Gerar ~/.toolboxrc", command=generate_toolboxrc)
button.pack(pady=10)

root.mainloop()
