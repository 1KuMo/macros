import pyautogui
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController  # // pour MouseController
import tkinter as tk
import time
import threading 
import webbrowser # Help window "skytoad GitHub"
from PIL import ImageGrab

#==============================================================
# window
#==============================================================
window = tk.Tk()
window.title("Macros")

#==============================================================
# variables
#==============================================================
kb = KeyboardController()
souris = MouseController()

run = False
pause = False  
rep = 0
th = None

#==============================================================
# actions de base
#==============================================================
def verif_pause(mouse=False):
    global pause, run
    if not pause :
        return run
    print('pause...')
    if mouse : souris.release(Button.left)
    while pause :
        time.sleep(0.1)
    print('reprise')
    if mouse : souris.press(Button.left)
    return run

def tenir(touche, duree, mouse=False):
    global run, pause
    kb.press(touche)
    t0 = time.time()
    temps = 0
    attente = 0
    temp = False

    while temps < duree :
        if not run :
            break
        if pause :
            if not temp :
                print('pause...')
                temp = True
            kb.release(touche)
            if mouse : souris.release(Button.left)
            t1 = time.time()
            while pause :
                time.sleep(0.1)
            attente += time.time() - t1
            kb.press(touche)
            if mouse : souris.press(Button.left)
        else :
            temps = time.time() - t0 - attente
        time.sleep(0.1)

    if temp :
        print('reprise')
    kb.release(touche)
    return run

def clic(btn, duree):
    if not run :
        return run
    souris.press(btn)
    time.sleep(duree)
    souris.release(btn)
    return run

#==============================================================
# macros farming
#==============================================================
def wart():
    global run, rep
    print('--- start wart ---')
    while run :
        if not verif_pause(True) : break
        souris.press(Button.left)
        if not tenir('q', 121, True) : break
        if not tenir('d', 121, True) : break
        if not tenir('q', 121, True) : break
        if not tenir('d', 121, True) : break
        if not tenir('q', 125, True) : break
        souris.release(Button.left)
        rep += 1
        print(f'rep {rep} fini')
    souris.release(Button.left)
    run = False
    print(f'--- fin wart | rep {rep} ---')
    rep = 0

def pump(): # UTILISE
    global run, rep
    print('--- start pump ---')
    while run :
        if not verif_pause(True) : break
        souris.press(Button.left)
        if not tenir('q', 74, True) : break
        if not tenir('d', 74, True) : break
        if not tenir('q', 74, True) : break
        if not tenir('z', 2, True) : break
        souris.release(Button.left)
        rep += 1
        print(f'rep {rep} fini')
    souris.release(Button.left)
    run = False
    print(f'--- fin pump | rep {rep} ---')
    rep = 0

def melon():
    global run, rep
    print('--- start melon ---')
    while run :
        if not verif_pause(True) : break
        souris.press(Button.left)
        if not tenir('d', 73, True) : break
        if not tenir('q', 73, True) : break
        if not tenir('d', 73, True) : break
        if not tenir('q', 73, True) : break
        if not tenir('d', 73, True) : break
        souris.release(Button.left)
        rep += 1
        print(f'rep {rep} fini')
    souris.release(Button.left)
    run = False
    print(f'--- fin melon | rep {rep} ---')
    rep = 0

#==============================================================
# macros foraging
#==============================================================
def acacia():
    global run, rep
    print('--- start acacia ---')
    while run :
        if not verif_pause() : break
        if not tenir('é', 0.15) : break
        if not clic(Button.right, 0.75) : break
        if not tenir('"', 0.15) : break
        if not clic(Button.right, 0.75) : break
        if not tenir('&', 0.15) : break
        if not clic(Button.left, 0.3) : break
        time.sleep(0.2)
        rep += 1
        print(f'rep {rep} fini')
    run = False
    print(f'--- fin acacia | rep {rep} ---')
    rep = 0

def oak():
    global run, rep
    print('--- start oak ---')
    while run :
        if not verif_pause() : break
        if not tenir('"', 0.15) : break
        if not clic(Button.right, 0.75) : break
        if not tenir('d', 0.4) : break
        if not tenir('"', 0.15) : break
        if not clic(Button.right, 0.75) : break
        if not tenir('q', 0.5) : break
        if not tenir('è', 0.2) : break
        if not clic(Button.right, 0.75) : break
        if not tenir('é', 0.15) : break
        if not clic(Button.left, 0.3) : break
        time.sleep(0.2)
        rep += 1
        print(f'rep {rep} fini')
    run = False
    print(f'--- fin oak | rep {rep} ---')
    rep = 0

def fish():
    global run, rep
    print('--- start fish ---')
    while run :
        if not verif_pause() : break
        if not tenir('w', 120) : break
        if not tenir('a', 120) : break
        if not tenir('s', 130) : break
        if not tenir('d', 100) : break
        rep += 1
        print(f'rep {rep} fini')
    run = False
    print(f'--- fin fish | rep {rep} ---')
    rep = 0

#==============================================================
# click farm
#==============================================================
def click():
    global run, rep
    print('--- start click ---')
    while run :
        if not verif_pause() : break
        souris.click(Button.left)
        time.sleep(0.2)
        rep += 1
    run = False

#==============================================================
# lancement / touches
#==============================================================
def start():
    global th, run
    if run :
        print('deja en cours')
        return
    if wart_var.get() :
        th = threading.Thread(target=wart)
    elif oak_var.get() :
        th = threading.Thread(target=oak)
    elif pump_var.get() :
        th = threading.Thread(target=pump)
    elif melon_var.get() :
        th = threading.Thread(target=melon)
    elif acacia_var.get() :
        th = threading.Thread(target=acacia)
    elif fish_var.get() :
        th = threading.Thread(target=fish)
    else :
        print('aucune macro')
        return
    run = True
    th.start()

def mouvements(touche):
    global run, pause, th
    try :
        if touche == Key.f5 : # start
            if not run : # si c'est pas deja start
                print('F5 start')
                start()
            else :
                print('F5 reprise')
                pause = False # if paused : start back
        elif hasattr(touche, 'char') and touche.char == 'x' : # macro click maths
            if not run :
                run = True
                th = threading.Thread(target=click)
                th.start()
            else : # stop if running
                run = False
        elif touche == Key.f8 : # pause / start back
            if run :
                pause = not pause
        elif touche == Key.f3 : # STOP
            if run :
                run = False
                pause = False
                if th is not None : th.join()
    except Exception as e :
        print(f'err : {e}')

radio = keyboard.Listener(on_press=mouvements)
radio.start()

#==============================================================
# interface
#==============================================================
font_large = ('Arial', 16)
font_title = ('Helvetica', 20, 'bold')
font_cat = ('New Romance', 13)

title_label = tk.Label(window, text='Bienvenue dans l\'interface', font=font_title)
title_label.pack(pady=10)

''' le label et Label ne sont pas les memes : un pour le nom de la variable qui contient le titre l'autre pour le texte '''

cat_label = tk.Label(window, text='---------------------------Farming---------------------------', font=font_cat)
cat_label.pack()

wart_var = tk.BooleanVar()
wart_box = tk.Checkbutton(window, text='Nether Wart Macro', variable=wart_var, font=font_large)
wart_box.pack()

pump_var = tk.BooleanVar()
pump_box = tk.Checkbutton(window, text='Pumpkin Macro', variable=pump_var, font=font_large)
pump_box.pack()

melon_var = tk.BooleanVar()
melon_box = tk.Checkbutton(window, text='Melon Macro / opti farm', variable=melon_var, font=font_large)
melon_box.pack()

click_var = tk.BooleanVar()
click_box = tk.Checkbutton(window, text='CLICK MACRO', variable=click_var, font=font_large)
click_box.pack()

cat_label = tk.Label(window, text='---------------------------Foraging---------------------------', font=font_cat)
cat_label.pack()

oak_var = tk.BooleanVar()
oak_box = tk.Checkbutton(window, text='Dark Oak Macro', variable=oak_var, font=font_large)
oak_box.pack()

acacia_var = tk.BooleanVar()
acacia_box = tk.Checkbutton(window, text='Acacia Macro', variable=acacia_var, font=font_large)
acacia_box.pack()

cat_label = tk.Label(window, text='---------------------------Fishing---------------------------', font=font_cat)
cat_label.pack()

fish_var = tk.BooleanVar()
fish_box = tk.Checkbutton(window, text='Trophy Fishing Macro', variable=fish_var, font=font_large)
fish_box.pack()

cat_label = tk.Label(window, text='---------------------------Enchanting---------------------------', font=font_cat)
cat_label.pack()

#==============================================================
# guide
#==============================================================
def guide():
    window_guide = tk.Toplevel(window)
    window_guide.title('Guide')
    window_guide.minsize(500, 400)
    label = tk.Label(window_guide, text='Bienvenue dans le guide !', font=('Arial', 22))
    label.pack(pady=20)
    cat_label = tk.Label(window_guide, text='------------------------------------------------------COMMANDES------------------------------------------------------', font=('Arial', 14))
    cat_label.pack()
    aide_label = tk.Label(window_guide, text='Afin d\'utiliser correctement MacroToad, voici quelques indications :', font=('Arial', 22))
    aide_label.pack(pady=20)
    txt_cmd = """Cochez premièrement la case correspondant à la macro souhaitée.\nF5 vous permettra de démarrer la macro sélectionnée.\nF8 vous permettra d'arrêter temporairement une macro en cours puis de la reprendre.\nF3 vous permettra d'arrêter la macro en cours / en pause."""
    cmd_label = tk.Label(window_guide, text=txt_cmd, font=('Arial', 18), justify='center')
    cmd_label.pack(pady=10)
    def lien():
        webbrowser.open('https://github.com/1KuMo/Skytoad')
    lien_label = tk.Label(window_guide, text='GitHub KuMo', font=('Arial', 16), fg='blue', cursor='hand2')
    lien_label.pack(pady=20)
    lien_label.bind('<Button-1>', lambda e : lien())

guide_button = tk.Button(window, text='Guide', font=('Arial', 14), command=guide)
guide_button.pack(pady=10)

window.minsize(400, 300)
window.mainloop()
