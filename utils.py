import re

def preprocess_message(text):
    text = text.upper()
    text = text.replace('À', 'A').replace('È', 'E').replace('É', 'E')
    text = text.replace('Í', 'I').replace('Ò', 'O').replace('Ó', 'O')
    text = text.replace('Ú', 'U').replace('Ü', 'U')
    return re.sub(r'[^A-Z]', '', text)

def format_output(cipher_text):
    return " ".join([cipher_text[i:i+5] for i in range(0, len(cipher_text), 5)])

def save_to_file(file_name, content):
    try:
        with open(file_name, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"[ERROR] Failed writing {file_name}: {e}")
        return False


