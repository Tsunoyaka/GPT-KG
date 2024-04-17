import numpy as np
from pydub import AudioSegment

def data_to_mp3():
    # Параметры аудиосигнала
    sample_rate = 44100  # Частота дискретизации (в Гц)
    duration = 2  # Длительность аудиосигнала (в секундах)
    frequency = 440  # Частота синусоиды (в Гц)

    # Создание массива аудиоданных (синусоиды)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = np.sin(2 * np.pi * frequency * t)

    # Преобразование в mp3

    # Преобразование массива данных в строку байт
    audio_bytes = (audio_data * 32767).astype(np.int16).tobytes()

    # Создание аудиосегмента
    audio_segment = AudioSegment(
        data=audio_bytes,
        sample_width=2,  # 2 байта на отсчет
        frame_rate=sample_rate,
        channels=1  # Монофонический сигнал
    )

    # Сохранение аудиосегмента в файл mp3
    output_filename = "sine_wave.mp3"
    audio_segment.export(output_filename, format="mp3")

    print("Аудиофайл успешно создан:", output_filename)