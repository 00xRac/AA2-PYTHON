from enigma_constants import ALPHABET

class Rotor:
    def __init__(self, index, wiring, notch="Z"):
        self.index = index
        self.wiring = wiring
        self.notch = notch.upper()
        self.position = 0
        self.inverse = get_inverse_wiring(wiring)

    def rotate(self):
        self.position = (self.position + 1) % 26

    def forward(self, ch):
        i = (ALPHABET.index(ch) + self.position) % 26
        c = self.wiring[i]
        return ALPHABET[(ALPHABET.index(c) - self.position) % 26]

    def backward(self, ch):
        i = (ALPHABET.index(ch) + self.position) % 26
        c = self.inverse[i]
        return ALPHABET[(ALPHABET.index(c) - self.position) % 26]

def validate_wiring(wiring):
    return len(wiring) == 26 and set(wiring) == set(ALPHABET)


def get_inverse_wiring(wiring):
    inv = [''] * 26
    for i, c in enumerate(wiring):
        inv[ALPHABET.index(c)] = ALPHABET[i]
    return "".join(inv)

def load_rotor(rotor_index):
    file_name = ROTOR_FILES[rotor_index - 1]
    try:
        with open(file_name, 'r') as f:
            lines = [line.strip().upper() for line in f.readlines()]
        wiring = lines[0] if len(lines) > 0 else ""
        notch = lines[1] if len(lines) > 1 and lines[1] else "Z"
        if not validate_wiring(wiring):
            print(f"[ERROR] Invalid wiring in {file_name}")
            return None
        return Rotor(rotor_index, wiring, notch)
    except FileNotFoundError:
        print(f"[ERROR] File {file_name} not found")
        return None
    except Exception as e:
        print(f"[ERROR] Failed reading {file_name}: {e}")
        return None

def save_rotor(rotor_index, wiring, notch):
    file_name = ROTOR_FILES[rotor_index - 1]
    try:
        with open(file_name, 'w') as f:
            f.write(wiring + '\n')
            f.write(notch + '\n')
        return True
    except Exception as e:
        print(f"[ERROR] Failed writing {file_name}: {e}")
        return False
