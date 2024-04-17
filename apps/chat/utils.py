import io
import os
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pytube import YouTube
from moviepy.editor import AudioFileClip
from .validates import is_valid_youtube_link
import moviepy.editor as mp
import requests
import json

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  
        
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU') 
            return text
        except sr.UnknownValueError:
            return "Не удалось распознать речь"
        except sr.RequestError as e:
            return f"Ошибка сервиса распознавания речи: {e}"
        except Exception as e:
            return f"Ошибка при определении языка: {e}"


def split_and_recognize(input_file, language):
    segment_length_ms=10000
    with io.BytesIO(input_file) as wav_file:
        wav_file.seek(0)
        audio = AudioSegment.from_wav(wav_file)
        total_duration = len(audio)
        segment_count = total_duration // segment_length_ms + 1
        
        recognizer = sr.Recognizer()
        
        full_text = ""
        for i in range(segment_count):
            start_time = i * segment_length_ms
            end_time = min((i + 1) * segment_length_ms, total_duration)
            segment = audio[start_time:end_time]
            
            segment_io = io.BytesIO()
            segment.export(segment_io, format="wav")
            segment_io.seek(0)
            
            try:
                with sr.AudioFile(segment_io) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language=language)
                    full_text += text + " "
            except sr.UnknownValueError:
                ...
        return full_text



def download_audio_as_wav(video_url):
    if is_valid_youtube_link(video_url):
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        # Скачиваем аудио во временный файл
        with io.BytesIO() as audio_buffer:
            audio_stream.stream_to_buffer(audio_buffer)
            audio_buffer.seek(0)

            # Создаем временный файл и записываем в него аудиоданные
            temp_audio_file = "temp_audio.mp4"
            with open(temp_audio_file, "wb") as f:
                f.write(audio_buffer.read())

            # Конвертация аудиодорожки из MP4 в WAV
            audio_clip = AudioFileClip(temp_audio_file)
            wav_temp_file = "temp_audio.wav"
            audio_clip.write_audiofile(wav_temp_file)

            # Читаем содержимое WAV файла в байтовый объект
            with open(wav_temp_file, "rb") as wav_file:
                wav_bytes = wav_file.read()
            
            # Удаляем временные файлы
            os.remove(temp_audio_file)
            os.remove(wav_temp_file)

            return wav_bytes
    else:
        return "Такого видео нет"
    
    
def process_video_and_recognize_text(mp4_file):
    wav_file = "temp.wav"  # временный WAV файл

    # Конвертация MP4 в WAV
    clip = mp.VideoFileClip(mp4_file)
    clip.audio.write_audiofile(wav_file)

    # Распознавание речи из аудиофайла
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        recognized_text = recognizer.recognize_google(audio_data, language="ru-RU")

    # Удаление временного WAV файла
    os.remove(wav_file)

    return recognized_text



def translate_text(text, src_lang, dest_lang='ky'):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    translated_text = translator.translate(text)
    return translated_text


def audio_kg(audio_file):
    url = "https://asr.ulut.kg/api/receive_data"

    payload = {}
    files = {'audio': audio_file}

    headers = {
        'Authorization': 'Bearer 37f1e7ea5d6515b79b0d29a0b0bd55ad480aa426c4ca242f9c715a1daf271aeffd62de26557935e706932e4a09580b8a5bf9556c5107bc2419eede9439bc7479'
    }

    response = requests.post(url, headers=headers, data=payload, files=files)
    data = json.loads(response.text)
    return data['text']


def audio_split_kg(audio_file):
    audio = AudioSegment.from_file(audio_file)

    # Делим аудиофайл на части по 10 секунд
    chunk_length_ms = 10000  # 10 секунд
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunks.append(chunk)

    # Отправляем каждый чанк на сервер и получаем результаты
    results = []
    for chunk in chunks:
        # Сохраняем временный файл для текущего чанка
        temp_file = "temp_chunk.mp3"
        chunk.export(temp_file, format="mp3")

        # Отправляем чанк на сервер
        url = "https://asr.ulut.kg/api/receive_data"
        headers = {
            'Authorization': 'Bearer 37f1e7ea5d6515b79b0d29a0b0bd55ad480aa426c4ca242f9c715a1daf271aeffd62de26557935e706932e4a09580b8a5bf9556c5107bc2419eede9439bc7479'
        }
        files = {'audio': open(temp_file, 'rb')}
        response = requests.post(url, headers=headers, files=files)

        # Добавляем результат в список результатов
        data = json.loads(response.text)
        results.append(data['text'])

    # Объединяем результаты в единую строку
    full_text = " ".join(results)

    return full_text

def text_to_audio(text):
    url = "http://tts.ulut.kg/api/tts"

    payload = json.dumps({
        "text": text,
        "speaker_id": 2
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 0vHR4OJS3meHiO5LiEMSRE8mpr09GAwwvSOlkT9rdLSewPD52TkQTa74Ve1yfc5wwMkMcPwOgOPsxGUOcFcZqAk4SAdzKM5rg0XQbRSVv8akhAJrPgg2ESZb0egrycYu01TP'
    }

    response = requests.post(url, headers=headers, data=payload)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем содержимое ответа
        audio_content = response.content
        return audio_content
