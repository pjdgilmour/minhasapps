import os
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tqdm import tqdm
import subprocess
import threading

def convert_videos():
    # Selecionar a pasta de origem
    source_folder = filedialog.askdirectory(title="Selecione a pasta de origem")
    if not source_folder:
        return

    # Criar a pasta "Convertidos" dentro da pasta de origem, se já não existir
    output_folder = os.path.join(source_folder, "Convertidos")
    os.makedirs(output_folder, exist_ok=True)

    # Obter a lista de arquivos .mp4 na pasta de origem
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(".mp4")]

    total_files = len(files)
    progress_var.set(0)
    progress_label.config(text="Convertendo vídeos: 0%")
    
    def update_progress(n):
        progress_var.set(n)
        progress_label.config(text=f"Convertendo vídeos: {n}%")
        root.update_idletasks()

    def convert():
        for i, file in enumerate(files):
            input_file = os.path.join(source_folder, file)
            output_file = os.path.join(output_folder, os.path.splitext(file)[0] + ".mov")

            # Verificar a resolução do vídeo de origem
            resolution = get_video_resolution(input_file)
            if resolution is None:
                log_text.insert(END, f"Erro ao obter resolução do vídeo: {input_file}\n")
                continue

            width, height = resolution

            # Verificar se a resolução é maior que Full HD (1920x1080)
            if width > 1920 or height > 1080:
                # Redimensionar para Full HD
                resize_args = ["-vf", "scale=1920:1080"]
                output_file = os.path.join(output_folder, os.path.splitext(file)[0] + "_HD.mov")
            else:
                resize_args = []

            # Comando FFmpeg para converter o vídeo
            ffmpeg_args = [
                "ffmpeg", "-i", input_file,
                *resize_args, 
                "-c:v", "dnxhd", 
                "-b:v", "45M",
                "-pix_fmt", "yuv422p", 
                "-c:a", "pcm_s16le", 
                output_file
            ]

            # Executar o comando FFmpeg e capturar a saída
            try:
                result = subprocess.run(ffmpeg_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                log_text.insert(END, result.stdout)
                log_text.insert(END, result.stderr)
            except subprocess.CalledProcessError as e:
                log_text.insert(END, f"Erro ao converter o vídeo: {input_file}\n")
                log_text.insert(END, e.stderr)

            update_progress(int(((i + 1) / total_files) * 100))

        log_text.insert(END, "Conversão concluída com sucesso!\n")
        messagebox.showinfo("Conversão Concluída", "Todos os vídeos foram convertidos com sucesso!")

    threading.Thread(target=convert).start()

def get_video_resolution(input_file):
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", input_file]
    try:
        output = subprocess.check_output(command).decode("utf-8").strip()
        width, height = map(int, output.split("x"))
        return width, height
    except subprocess.CalledProcessError:
        return None

# Configuração da interface
root = Tk()
root.title("Conversor de Vídeo")
root.geometry("600x500")

# Botão para iniciar a conversão
convert_button = Button(root, text="Converter Vídeos", command=convert_videos)
convert_button.pack(pady=20)

# Barra de progresso
progress_var = DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var, maximum=100)
progress_bar.pack(pady=10)

progress_label = Label(root, text="Convertendo vídeos: 0%")
progress_label.pack()

# Caixa de texto para exibir o log
log_text = scrolledtext.ScrolledText(root, wrap=WORD, width=70, height=15)
log_text.pack(pady=20)

# Botão para sair
exit_button = Button(root, text="Sair", command=root.quit)
exit_button.pack(pady=10)

root.mainloop()