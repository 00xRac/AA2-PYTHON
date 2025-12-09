from enigma_constants import ALPHABET
from rotor_manager import load_rotor

class EnigmaMachine:
    def __init__(self, initial_setting="AAA"):
        """
        Inicializa la màquina carregant els 3 rotors.
        """
        self.rotors = []
        # Carreguem els rotors 1, 2 i 3
        for i in range(1, 4):
            r = load_rotor(i)
            if r is None:
                raise ValueError(f"Error carregant Rotor {i}")
            self.rotors.append(r)
        
        # Configurem les posicions inicials
        self.set_rotor_positions(initial_setting)

    def set_rotor_positions(self, setting):
        """
        Posa els rotors a la posició inicial (ex: 'A B C').
        """
        if len(setting) != 3: 
            return # Error silenciós o print, però assumim validació prèvia
            
        for i, char in enumerate(setting):
            if char in ALPHABET:
                self.rotors[i].position = ALPHABET.index(char)

    def step_rotors(self):
        """
        Lògica de pas (Odòmetre):
        R1 sempre gira. R2 gira si R1 està al notch. R3 gira si R2 està al notch.
        """
        r1, r2, r3 = self.rotors[0], self.rotors[1], self.rotors[2]

        moure_r2 = False
        moure_r3 = False

        # Comprovem els notches ABANS de moure res
        if ALPHABET[r1.position] == r1.notch:
            moure_r2 = True
        
        if moure_r2 and ALPHABET[r2.position] == r2.notch:
            moure_r3 = True

        # Apliquem el moviment
        r1.rotate()
        if moure_r2: r2.rotate()
        if moure_r3: r3.rotate()

    def process_text(self, text, mode='encrypt'):
        """
        Processa tot el text lletra a lletra.
        """
        resultat = []
        for char in text:
            if char not in ALPHABET:
                continue
            
            # 1. Moure rotors
            self.step_rotors()
            
            # 2. Passar senyal
            lletra_actual = char
            
            if mode == 'encrypt':
                # Anada: R1 -> R2 -> R3
                for rotor in self.rotors:
                    lletra_actual = rotor.forward(lletra_actual)
            else:
                # Tornada (Desxifrar): R3 -> R2 -> R1 (invers)
                for rotor in reversed(self.rotors):
                    lletra_actual = rotor.backward(lletra_actual)
            
            resultat.append(lletra_actual)
        
        return "".join(resultat)