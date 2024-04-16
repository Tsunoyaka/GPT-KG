import google.generativeai as genai

genai.configure(api_key="AIzaSyDprGrlJ0grgoa-Gm8K2E5UB_XaMcEWqU4")  # Замените на ваш API-ключ
model = genai.GenerativeModel('gemini-pro')

def gemimi_answer(message):
    response = model.generate_content(message)
    re_responce = response.text.replace("*", '')
    return re_responce