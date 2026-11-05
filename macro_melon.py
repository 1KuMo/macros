import time
import os
import random
import threading
import pygame 
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

#initialisation audio
pygame.mixer.init()
son_cloche = r"" # à changer

kb = KeyboardController()
souris = MouseController()

run = False
pause = False
pet_run = False 
rep = 0

tab_down = [
    (KeyCode.from_char('a'), 0.1), (KeyCode.from_char('c'), 0.12), 
    (KeyCode.from_char('"'), 0.18), ("rightclick", 0.11), 
    (KeyCode.from_char('&'), 0.17), (Key.shift, 0.2),
    (Key.caps_lock, 0.19)
]

tab_up = [
    (KeyCode.from_char('p'), 0.16), (Key.shift, 0.12),
    (KeyCode.from_char('c'), 0.14), (KeyCode.from_char('é'), 0.15)
]

tab_pet = [
    (KeyCode.from_char('"'), 0.11), ("rightclick", 0.12), (KeyCode.from_char('é'), 0.1)
]

def relacher():
    for c in ['q', 's', 'a', 'c', 'p', 'é']:
        try:
            kb.release(KeyCode.from_char(c))
        except:
            pass
    kb.release(Key.shift)
    kb.release(Key.ctrl_l)
    souris.release(Button.left)
    souris.release(Button.right)

def go(tab):
    global pet_run
    relacher()
    time.sleep(0.2)
    for touche, duree in tab:
        if touche == Key.shift and duree == 0.2:
            kb.press(touche)
            time.sleep(duree - 0.05)
            souris.press(Button.right)
            time.sleep(duree - 0.08)
            souris.release(Button.right)
            time.sleep(duree)
            kb.release(touche)
        elif touche == "rightclick":
            souris.press(Button.right)
            time.sleep(duree)
            souris.release(Button.right)
        else:
            kb.press(touche)
            time.sleep(duree)
            kb.release(touche)
            
            if touche == KeyCode.from_char('é') and duree == 0.15:
                if not pet_run:
                    print("--- time 110 ---")
                    pet_run = True
                    threading.Thread(target=pet, daemon=True).start()
                    
        time.sleep(0.12)

def relance():
    global pause
    go(tab_up)
    time.sleep(0.2)
    pause = False
    print("--- reprise macro ---")

def pet():
    global pause, run, pet_run
    try:
        for i in range(110):
            if not run:
                return
            time.sleep(1)
        
        if run:
            print("--- change pet ---")
            pause = True 
            time.sleep(0.5)

            go(tab_pet) 
            
            time.sleep(0.2)
            try:
                pygame.mixer.music.load(son_cloche)
                pygame.mixer.music.play()
            except:
                print("Erreur audio")
            
            time.sleep(1)
            pause = False 
            print("--- fin pet ---")
            
    finally:
        pet_run = False

def macro():
    global run, pause, rep
    print("START MACRO")
    
    while run:
        for c in ['q', 's']:
            if not run: break
            
            touche = KeyCode.from_char(c)
            duree = random.uniform(19.0, 20.5)
            temps = 0
            
            if not pause:
                souris.press(Button.left)
                kb.press(touche)
                print(f"debut dir : {c}")

            while temps < duree and run:
                if not pause:
                    time.sleep(0.1)
                    temps += 0.1
                else:
                    print("Pause en cours (PET)...")
                    kb.release(touche)
                    souris.release(Button.left)
                    
                    while pause and run:
                        time.sleep(0.1)
                    
                    if run:
                        print(f"REPRISE MINAGE : {c}")
                        time.sleep(0.5)
                        souris.press(Button.left)
                        time.sleep(0.1)
                        kb.press(touche)
            
            kb.release(touche)
            
        rep += 1
        print(f"rep {rep} fini")

    relacher()

def mouvements(key):
    global run, pause
    try:
        if key == Key.f5:
            if not run:
                run = True
                pause = False
                threading.Thread(target=macro, daemon=True).start()
        
        elif key == Key.ctrl_l:
            if run and not pause:
                pause = True
                threading.Thread(target=lambda: go(tab_down), daemon=True).start()
        
        elif key == KeyCode.from_char('w'):
            if pause:
                threading.Thread(target=relance, daemon=True).start()
        
        elif key == Key.f4:
            print("STOP MACRO")
            run = False
            pause = False
            relacher()
            os._exit(0)
    except:
        pass

with keyboard.Listener(on_press=mouvements) as radio:
    radio.join()
