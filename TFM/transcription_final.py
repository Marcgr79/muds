import os
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment

# Función para dividir el audio en partes más pequeñas
def split_audio(file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_wav(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

# Función para transcribir un archivo de audio y devolver la transcripción
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data, language="en-EN")
    return transcript

# Función para transcribir un video y guardar la transcripción en un archivo de texto
def transcribe_video(video_path):
    try:
        # Extraer el audio del video
        video = mp.VideoFileClip(video_path)
        audio = video.audio

        # Definir el nombre del archivo de audio y TXT
        audio_filename = os.path.splitext(os.path.basename(video_path))[0]
        temp_audio_path = audio_filename + ".wav"
        txt_filename = audio_filename + ".txt"

        # Guardar el audio en un archivo temporal
        audio.write_audiofile(temp_audio_path)

        # Dividir el archivo de audio en partes más pequeñas
        audio_chunks = split_audio(temp_audio_path)

        # Transcribir cada parte y combinar las transcripciones
        full_transcript = ""
        for i, chunk in enumerate(audio_chunks):
            chunk_path = f"{audio_filename}_chunk{i}.wav"
            chunk.export(chunk_path, format="wav")
            transcript = transcribe_audio(chunk_path)
            full_transcript += transcript + " "
            os.remove(chunk_path)

        # Eliminar el archivo temporal de audio
        os.remove(temp_audio_path)

        # Obtener la ruta de la carpeta del video
        video_folder = os.path.dirname(video_path)

        # Guardar la transcripción en un archivo TXT en la misma carpeta que el video
        txt_path = os.path.join(video_folder, txt_filename)
        with open(txt_path, mode='w', encoding='utf-8') as file:
            file.write(full_transcript)

        return full_transcript
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except Exception as e:
        print(f"An error occurred: {e}")

# Ruta a la carpeta que contiene los videos
folder_path = "C:/Users/Marc/Desktop/Master/TFM/cutted_feedback/english/failed"

# Iterar sobre los archivos en la carpeta
for filename in os.listdir(folder_path):
    # Comprobar si el archivo es un video (por su extensión)
    if filename.endswith(".mp4"):
        # Construir la ruta completa al video
        video_path = os.path.join(folder_path, filename)
        
        # Transcribir el video y guardar la transcripción en un archivo de texto
        transcript = transcribe_video(video_path)
        
        if transcript:
            # Construir la ruta completa al archivo de texto
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(folder_path, txt_filename)
            
            # Guardar la transcripción en el archivo de texto
            with open(txt_path, mode='w', encoding='utf-8') as file:
                file.write(transcript)

            print(f"Transcripción del video {filename} guardada en {txt_filename}")
        else:
            print(f"Failed to transcribe video {filename}")
