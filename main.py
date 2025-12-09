import os
import signal
from enigma_constants import ALPHABET, ROTOR_FILES, ENCRYPTED_FILE, DECRYPTED_FILE
from enigma_core import EnigmaMachine
from utils import preprocess_message, format_output, save_to_file
from rotor_manager import save_rotor, validate_wiring

def handle_sigint(signum, frame):
    print("\n\n[!] Sortind...")
    exit(0)
    
signal.signal(signal.SIGINT, handle_sigint)

def demanar_posicio_inicial():
    """
    Pregunta a l'usuari la posició dels 3 rotors (ex: A B C).
    Controla que siguin 3 lletres vàlides.
    """
    while True:
        entrada = input("Introdueix posició inicial (3 lletres, ex: 'A B C'): ").upper()
        # Treiem els espais per si l'usuari posa "A B C" o "ABC"
        lletres = entrada.replace(" ", "")
        
        if len(lletres) == 3 and all(c in ALPHABET for c in lletres):
            return lletres
        else:
            print("[ERROR] Has d'introduir exactament 3 lletres (A-Z). Torna-ho a provar.")

def main():
    continuar = True
    while continuar:
        # Menú principal
        print("\n" + "="*40)
        print("      ENIGMA SIMULATOR (M3)")
        print("="*40)
        print("1. Xifrar missatge")
        print("2. Desxifrar missatge")
        print("3. Editar rotors")
        print("4. Sortir")
        
        opcio = input("\nSelecciona una opció: ")

        # --- 1. XIFRAR MISSATGE ---
        if opcio == '1':
            print("\n--- XIFRATGE ---")
            
            # Comprovem que existeix el fitxer d'entrada
            if not os.path.exists("Missatge.txt"):
                print("[ERROR] No trobo el fitxer 'Missatge.txt'. Crea'l abans de començar.")
                continue

            try:
                # Llegim el missatge original
                with open("Missatge.txt", 'r', encoding='utf-8') as f:
                    text_original = f.read()
                
                # Netegem el text (treure accents, espais, etc.)
                text_net = preprocess_message(text_original)
                print(f"Text a processar ({len(text_net)} lletres): {text_net[:30]}...")

                # Configurem la màquina
                posicio = demanar_posicio_inicial()
                maquina = EnigmaMachine(initial_setting=posicio)

                # Xifrem
                text_xifrat = maquina.process_text(text_net, mode='encrypt')

                # Format militar (grups de 5)
                resultat_final = format_output(text_xifrat)
                
                # Guardem a disc
                if save_to_file(ENCRYPTED_FILE, resultat_final):
                    print(f"[OK] Missatge guardat correctament a '{ENCRYPTED_FILE}'")

            except Exception as e:
                print(f"[ERROR] Alguna cosa ha fallat durant el xifratge: {e}")

        # --- 2. DESXIFRAR MISSATGE ---
        elif opcio == '2':
            print("\n--- DESXIFRATGE ---")
            
            if not os.path.exists(ENCRYPTED_FILE):
                print(f"[ERROR] No existeix el fitxer '{ENCRYPTED_FILE}'. Has de xifrar alguna cosa primer.")
                continue

            try:
                # Llegim el fitxer xifrat
                with open(ENCRYPTED_FILE, 'r') as f:
                    contingut = f.read()
                
                # IMPORTANT: Treure els espais dels grups de 5 per poder desxifrar lletra a lletra
                text_entrada = contingut.replace(" ", "").strip()

                posicio = demanar_posicio_inicial()
                maquina = EnigmaMachine(initial_setting=posicio)

                # Desxifrem (mode decrypt fa servir el camí invers dels rotors)
                text_pla = maquina.process_text(text_entrada, mode='decrypt')

                if save_to_file(DECRYPTED_FILE, text_pla):
                    print(f"[OK] Missatge recuperat guardat a '{DECRYPTED_FILE}'")
                    print(f"Missatge: {text_pla[:50]}...")

            except Exception as e:
                print(f"[ERROR] Alguna cosa ha fallat durant el desxifratge: {e}")

        # --- 3. EDITAR ROTORS ---
        elif opcio == '3':
            print("\n--- EDITOR DE ROTORS ---")
            rotor_num = input("Quin rotor vols canviar? (1, 2 o 3): ")
            
            if rotor_num in ['1', '2', '3']:
                print(f"Configurant Rotor {rotor_num}...")
                nou_wiring = input("Introdueix la nova permutació (26 lletres úniques): ").upper().strip()

                if validate_wiring(nou_wiring):
                    notch = input("Introdueix la lletra de notch (salt): ").upper().strip()
                    # Si l'usuari no posa res, per defecte és Z (com diu el PDF)
                    if not notch or notch not in ALPHABET:
                        notch = "Z"
                        print("Avis: S'ha assignat el notch 'Z' per defecte.")
                    
                    # Guardem fent servir la funció que ja tenim al rotor_manager
                    if save_rotor(int(rotor_num), nou_wiring, notch):
                        print(f"[OK] Rotor {rotor_num} actualitzat.")
                else:
                    print("[ERROR] La permutació no és vàlida. Ha de tenir 26 lletres sense repetir.")
            else:
                print("[ERROR] Opció incorrecta. Només hi ha rotors 1, 2 o 3.")

        # --- 4. SORTIR ---
        elif opcio == '4':
            print("Tancant el simulador... Fins aviat!")
            continuar = False
        
        else:
            print("Opció no reconeguda. Si us plau, tria 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()
