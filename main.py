import os
import signal
from enigma_constants import ALPHABET, ENCRYPTED_FILE, DECRYPTED_FILE
from enigma_core import EnigmaMachine
from utils import preprocess_message, format_output, save_to_file
from rotor_manager import save_rotor, validate_wiring, load_rotor

#Codi de CTRL+C extret del streamer/hacker s4vitar.
def handle_sigint(signum, frame):
    print("\n\n[!] Sortint ...")
    exit(0)
    
signal.signal(signal.SIGINT, handle_sigint)

ROTORS = [None] * 3

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

def load_all_rotors():
    all_ok = True
    for i in range(1, 4):
        r = load_rotor(i)
        ROTORS[i-1] = r
        if r is None: all_ok = False
    return all_ok

def edit_rotors_option():
    print("\n--- Editar Rotors ---")
    try:
        idx = int(input("Quin rotor vols editar? (1-3): "))
        if idx not in [1, 2, 3]:
            print("[ERROR] Index invalid")
            return
    except ValueError:
        print("[ERROR] Input invalid")
        return
    wiring = input("Nou cablejat de 26 lletres: ").upper().strip()
    print(wiring)
    if validate_wiring(wiring):
        old_rotor = ROTORS[idx-1]
        default_notch = old_rotor.notch if old_rotor else "Z"
        notch_input = input(f"Nova marca (En blanc per {default_notch}): ").strip().upper()
        notch = notch_input if notch_input in ALPHABET else default_notch

        if save_rotor(idx, wiring, notch):
            print(f"[OK] Rotor {idx} actualitzat.")
            load_all_rotors()
    else:
        print("[ERROR] El cablejat ha de contenir 26 lletres úniques A-Z")

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
            # Demanem al usuari que intrudueixi el missatge
            entrada_usuari = input("Introdueix el missatge a xifrar: ")

            # Guardem el missatge en el fitxer
            with open("Missatge.txt", 'w', encoding='utf-8') as f:
                f.write(entrada_usuari)
            print("[INFO] Missatge guardat temporalment a 'Missatge.txt'.")

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
                    # Calculem les estadistiques arrodonint cap amunt
                    num_lletres = len(text_xifrat)
                    num_grups = (num_lletres + 4) // 5
                    print(f"[OK] Missatge guardat correctament a '{ENCRYPTED_FILE}' ({num_lletres} lletres, {num_grups} grups de 5)")

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
                    blocks = [text_pla[i:i+5] for i in range(0, len(text_pla), 5)]
                    formatted_text = " ".join(blocks)
                    
                    print(f"[OK] Missatge recuperat guardat a '{DECRYPTED_FILE}'")
                    print(f"Missatge: {formatted_text}")

            except Exception as e:
                print(f"[ERROR] Alguna cosa ha fallat durant el desxifratge: {e}")

        # --- 3. EDITAR ROTORS ---
        elif opcio == '3':
            edit_rotors_option()

        # --- 4. SORTIR ---
        elif opcio == '4':
            print("Tancant el simulador... Fins aviat!")
            continuar = False
        
        else:
            print("Opció no reconeguda. Si us plau, tria 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()
