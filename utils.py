import re

def preprocess_message(text):
    text = text.upper()
    text = text.replace('À', 'A').replace('È', 'E').replace('É', 'E')
    text = text.replace('Í', 'I').replace('Ò', 'O').replace('Ó', 'O')
    text = text.replace('Ú', 'U').replace('Ü', 'U')
    return re.sub(r'[^A-Z]', '', text)



