import os
from docx2pdf import convert
from PyPDF2 import PdfReader
import requests
import json
from pydub import AudioSegment
from io import BytesIO
import pythoncom
import tempfile


def count_pages_pdf(docx_file):
    pdf_file = convert(docx_file)
    with open(pdf_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
    os.remove(pdf_file)
    return num_pages

def my_extract_text(docx_file, page_number):
    pythoncom.CoInitialize()
    convert(docx_file)
    pythoncom.CoUninitialize()
    pdf_file = docx_file[:-5]+'.pdf'
    dict_ = {}
    with open(pdf_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        page = pdf_reader.pages[page_number - 1]
        dict_['pdf_file'] = pdf_file
        dict_['page_text']  = page.extract_text()
    
    return dict_
    
def split_text(text, chunk_size=900):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


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
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

def merge_audio(audio_segments):
    output = AudioSegment.silent(duration=0)
    for segment in audio_segments:
        output += segment
    return output

def main(docx_file, page_number):
    file_text = my_extract_text(docx_file, page_number)
    os.remove(file_text['pdf_file'])
    text_chunks = split_text(file_text['page_text'])
    audio_segments = []
    for chunk in text_chunks:
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            audio_data = text_to_audio(chunk)
            # temp_file.write(audio_data.getvalue())
            # temp_file_path = temp_file.name
            audio_stream = BytesIO(audio_data.getvalue())

        
            if audio_data:
                audio_segments.append(AudioSegment.from_file(audio_stream))
                # os.unlink(temp_file_path)

                break
    # output_audio = merge_audio(audio_segments)
    # output_audio.export("output_audio.mp3", format="mp3")
    
# with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
#     temp_file.write(audio_data)
#     temp_file_path = temp_file.name

# # Создаем аудиосегмент из временного файла
# audio_segment = AudioSegment.from_file(temp_file_path)

# # Удаляем временный файл
# os.unlink(temp_file_path)

# # Добавляем аудиосегмент в список
# audio_segments.append(audio_segment)
