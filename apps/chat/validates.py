import os
import re
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
   

