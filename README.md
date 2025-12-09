````
[........     [...     [..     [..        [....        [..       [..           [.       
[..           [. [..   [..     [..      [.    [..      [. [..   [...          [. ..     
[..           [.. [..  [..     [..     [..             [.. [.. [ [..         [.  [..    
[......       [..  [.. [..     [..     [..             [..  [..  [..        [..   [..   
[..           [..   [. [..     [..     [..   [....     [..   [.  [..       [...... [..  
[..           [..    [. ..     [..      [..    [.      [..       [..      [..       [.. 
[........     [..      [..     [..       [.....        [..       [..     [..         [..                                                                                   
````                                                                                                                                                                        
                                                                     
                     E N I G M A   S I M U L A T O R                
                      KRIEGSMARINE EDITION - M3                     
                                                                     
             "Die Sicherheit des Reiches ist unsere Pflicht"         
                 (The Security of the Reich is our Duty)            
                                                                     
_____________________________________________________________________        

## 1. Objectiu i Context
Aquest projecte consisteix en la simulació de la màquina **ENIGMA** (model M3 utilitzat per la Wehrmacht/Kriegsmarine). L'objectiu és reproduir la lògica dels seus rotors per protegir les comunicacions, aplicant els conceptes de xifratge per substitució polialfabètica definits per l'enginyer Arthur Scherbius el 1918.

El simulador implementa el comportament de **tres rotors** amb moviment independent, per transformar missatges de text de manera reversible.

## 2. Estructura del Projecte

* **`main.py`**: Punt d'entrada. Gestiona el menú principal i la interacció amb l'usuari.
* **`enigma_core.py`**: Conté la lògica central de la màquina (coordinació dels 3 rotors).
* **`rotor_manager.py`**: Defineix la classe `Rotor` i gestiona la càrrega/guardat de fitxers de rotors.
* **`utils.py`**: Funcions auxiliars per al processament de cadenes (neteja d'accents, espais) i gestió d'errors d'E/S.
* **`enigma_constants.py`**: Constants globals com l'alfabet i noms de fitxers predefinits.

## 3. Funcionament i Menú
En executar el programa (`python main.py`), es mostrarà el següent menú interactiu:

1.  **Xifrar missatge**: Llegeix `Missatge.txt`, processa el text i genera `Xifrat.txt`.
2.  **Desxifrar missatge**: Llegeix `Xifrat.txt`, aplica la lògica inversa i genera `Desxifrat.txt`.
3.  **Editar rotors**: Permet introduir manualment noves permutacions per als rotors.
4.  **Sortir**: Tanca l'aplicació.

### Configuració Inicial (Window Setting)
Abans de xifrar o desxifrar, el sistema demanarà la **posició inicial dels rotors** (tres lletres, p. ex., `A B C`). Aquestes actuen com les "finestres" visibles a la màquina original.

## 4. Gestió de Fitxers (Input/Output)

### Fitxers de Rotors (`Rotor1.txt`, `Rotor2.txt`, `Rotor3.txt`)
Cada fitxer defineix la configuració d'un rotor i ha de contenir dues línies:
1.  **Cablejat (Wiring):** Una permutació de 26 lletres majúscules (A-Z) sense repeticions.
2.  **Notch (posició de clau):** La lletra que fa avançar el següent rotor (si s'omet, s'assumeix 'Z').
    * *Exemple:*
      ```text
      EKMFLGDQVZNTOWYHXUSPAIBRCJ (Wiring)
      Q (notch)
      ```

### Fitxers de Missatges
* **Entrada (`Missatge.txt`):** Text en llenguatge natural. El programa convertirà automàticament a majúscules i eliminarà espais, accents i signes de puntuació.
* **Sortida Xifrada (`Xifrat.txt`):** El text resultant agrupat en blocs de 5 lletres separats per espais (format militar).
    * *Exemple:* `WRTXA ZMCHH ...`
* **Sortida Desxifrada (`Desxifrat.txt`):** Text recuperat en majúscules continuades.

## 5. Notes Tècniques i Disseny
Tot i que no hem donat el concepte de **Programació Orientada a Objectes (POO)** a classe, hem decidit utilitzar les classes (`Rotor`, `EnigmaMachine`) per encapsular l'estat i comportament de cada component. Això ens ha permès:
* Facilitar l'escalabilitat (afegir més rotors si calgués).
* Simplificar la lògica de l'efecte "odòmetre" (pas dels rotors).

## 6. Autors
* **Oscar Ferre Obon**
* **Joel Díaz Serrano**
