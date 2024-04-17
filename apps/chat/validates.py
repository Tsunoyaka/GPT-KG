import os
import requests
from django.core.exceptions import ValidationError

def validate_mp3(value):
    ext = os.path.splitext(value.name)[1]
    
    if ext.lower() != '.mp3':
        raise ValidationError('Только mp3')

def validate_mp4(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.mp4':
        raise ValidationError('Принимает только mp4')  
    

def check_path(text):
    if text.endswith('/') and text[-2].isdigit():
        return True
    else:
        return False

def is_youtube_link(text):
    return text.startswith("https://www.youtube.com/")

def is_valid_youtube_link(link):
    try:
        response = requests.head(link)
        return response.status_code == 200 and 'youtube.com' in response.url
    except requests.RequestException:
        return False
    
def is_string(obj):
    return isinstance(obj, str)