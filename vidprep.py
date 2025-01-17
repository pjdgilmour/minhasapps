import os
import subprocess
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

# Definir as extensões de vídeo suportadas
video_extensions = ['.mp4', '.mov', '.mts', '.MP4', '.MOV', '.MTS']

class VideoConverter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Conversor de Vídeos")
        # Janela principal
        self.set_border_width(10)
        self.set_default_size(300, 150)
        # Caixa vertical
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        # Caixa de seleção para escolher o formato de saída
        self.format_box = Gtk.ComboBoxText()
        self.format_box.append_text("WAV")
        self.format_box.append_text("MP3")
        self.format_box.set_active(0)  # Definir WAV como padrão
        vbox.pack_start(self.format_box, True, True, 0)
        # Botão para iniciar a conversão
        self.button = Gtk.Button(label="Converter Vídeos")
        self.button.connect("clicked", self.on_convert_clicked)
        vbox.pack_start(self.button, True, True, 0)
        # Barra de progresso
        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)
        # Label para mensagens
        self.status_label = Gtk.Label(label="Aguardando...")
        vbox.pack_start(self.status_label, True, True, 0)
        # Para garantir que a interface continue responsiva
        self.processing_thread = None

    def on_convert_clicked(self, widget):
        # Desativar o botão durante a conversão
        self.button.set_sensitive(False)
        self.status_label.set_text("Convertendo...")
        # Iniciar a conversão em uma thread separada
        self.processing_thread = threading.Thread(target=self.convert_videos)
        self.processing_thread.start()

    def update_progress(self, fraction, text):
        GLib.idle_add(self.progressbar.set_fraction, fraction)
        GLib.idle_add(self.progressbar.set_text, text)

    def set_status(self, text):
        GLib.idle_add(self.status_label.set_text, text)

    def convert_videos(self):
        # Diretório atual de trabalho
        video_folder = os.getcwd()
        videos = [f for f in os.listdir(video_folder) if os.path.splitext(f)[1] in video_extensions]
        
        total_videos = len(videos)
        if total_videos == 0:
            self.set_status("Nenhum vídeo encontrado.")
            GLib.idle_add(self.button.set_sensitive, True)
            return
        
        output_format = self.format_box.get_active_text().lower()
        
        for index, file in enumerate(videos):
            file_path = os.path.join(video_folder, file)
            
            # Verificar se o codec de áudio já está no formato desejado
            if self.is_audio_in_format(file_path, output_format):
                print(f'O arquivo {file} já está no formato {output_format.upper()}. Pulando...')
                continue
            
            # Criar um caminho temporário para o arquivo de saída em formato .mov
            temp_output_file = os.path.splitext(file_path)[0] + '_temp.mov'
            
            # Determinar o codec de áudio com base no formato escolhido
            audio_codec = 'pcm_s16le' if output_format == 'wav' else 'libmp3lame'
            
            # Comando FFmpeg para converter o áudio e manter o codec de vídeo original
            command = [
                'ffmpeg',
                '-i', file_path,              # Arquivo de entrada
                '-c:v', 'copy',               # Manter o codec de vídeo original
                '-c:a', audio_codec,          # Converter o codec de áudio
                '-threads', '0',              # Usar todos os núcleos disponíveis
                '-f', 'mov',                  # Forçar o formato de saída para .mov
                temp_output_file              # Arquivo temporário de saída em formato .mov
            ]
            
            print(f'Convertendo: {file_path}')
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Verificar se o arquivo temporário foi criado e substituir o original
            if os.path.exists(temp_output_file):
                os.remove(file_path)  # Apagar o arquivo original
                os.rename(temp_output_file, file_path.replace(os.path.splitext(file_path)[1], '.mov'))  # Renomear o arquivo temporário para .mov

            # Atualizar a barra de progresso
            fraction = (index + 1) / total_videos
            self.update_progress(fraction, f"{int(fraction * 100)}%")
        # Exibir mensagem de conclusão
        self.set_status("Conversão concluída!")
        GLib.idle_add(self.button.set_sensitive, True)
    
    def is_audio_in_format(self, file_path, output_format):
        # Usar FFprobe para verificar o formato do áudio
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        audio_codec = result.stdout.decode().strip().lower()
        
        if output_format == 'wav':
            return audio_codec == 'pcm_s16le'
        elif output_format == 'mp3':
            return audio_codec == 'mp3'
        return False

# Função principal para iniciar a interface GTK
def main():
    app = VideoConverter()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()