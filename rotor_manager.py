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
