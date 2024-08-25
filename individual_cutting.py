from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

# Ruta al archivo de video que deseas cortar
input_video = r"C:\Users\Marc\Desktop\Master\TFM\videos_totales\Elon DENUNCIA a Open AI NUEVO COWORKING y SUBIDA del Bitcoin  Jueves de itnig.mp4"
# Convertir las barras invertidas en la ruta de archivo a barras inclinadas hacia adelante
input_video_path = input_video.replace("\\", "/")

# Tiempo de inicio del recorte en minutos y segundos 
start_time_minutes = 86
start_time_seconds = 42

# Punto de inicio del recorte en segundos
start_time = start_time_minutes * 60 + start_time_seconds

# Duración del recorte en segundos (Ejemplo 3 minutos y 50 segundos)
cut_duration = 2 * 60 + 56

# Ruta a la carpeta donde guardar el recorte
output_folder = 'C:/Users/Marc/Desktop/Master/TFM/cutted_feedback'

# Asegúrate de que la carpeta de salida exista, si no, créala
os.makedirs(output_folder, exist_ok=True)

# Nombre del archivo de video de salida
output_video_name = 'Theker_Robotics_cut_feedback.mp4'

# Ruta completa del archivo de video de salida
output_video_path = os.path.join(output_folder, output_video_name)

# Extrae el recorte y guárdalo en la carpeta de salida
ffmpeg_extract_subclip(input_video_path, start_time, start_time + cut_duration, targetname=output_video_path)

print("¡Recorte completado!")
