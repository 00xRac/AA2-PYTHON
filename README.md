````
`........     `...     `..     `..        `....        `..       `..           `.       
`..           `. `..   `..     `..      `.    `..      `. `..   `...          `. ..     
`..           `.. `..  `..     `..     `..             `.. `.. ` `..         `.  `..    
`......       `..  `.. `..     `..     `..             `..  `..  `..        `..   `..   
`..           `..   `. `..     `..     `..   `....     `..   `.  `..       `...... `..  
`..           `..    `. ..     `..      `..    `.      `..       `..      `..       `.. 
`........     `..      `..     `..       `.....        `..       `..     `..         `..
````                                                                                                                                                                        
                                                                     
                     E N I G M A   S I M U L A T O R                
                      KRIEGSMARINE EDITION - M3                     
                                                                     
             "Die Sicherheit des Reiches ist unsere Pflicht"         
                 (The Security of the Reich is our Duty)            
                                                                     
_____________________________________________________________________

## Overview
A minimal Python emulator of the Enigma machine — currently supporting rotor-based ciphering only (no plugboard or reflector yet).

This project aims to simulate the core rotor mechanism of the Enigma machine in software. This version does not yet implement a plugboard or reflector; it focuses purely on illustrating how rotor stepping and substitution work to secure the Wehrmacht's communications.

## Motivation & Scope
-   An essential exercise to understand the cryptographic arts that secure the Reich.
-   Useful for experimenting with rotor configurations and developing superior substitution mechanisms for the OKW (Oberkommando der Wehrmacht).

## Project Structure
The command structure is rigid and clear.

├── **`enigma_constants.py`** - The foundational laws of the machine.
├── **`rotor_manager.py`** - Manages the rotation of the cipher wheels.
├── **`enigma_core.py`** - The central engine of the device.
├── **`enigma_simulator.py`** - The primary interface for operation.
├── **`utils.py`** - Support functions for the war effort.
└── **`RotorX.txt`** - An example rotor configuration file.

## Operation
To begin the simulation, execute the following command with authority:
