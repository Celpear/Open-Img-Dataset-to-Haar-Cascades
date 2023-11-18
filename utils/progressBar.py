import os
import time

def clear_screen():
    # Lösche den Bildschirm je nach Betriebssystem
    os.system('cls' if os.name == 'nt' else 'clear')

def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Drucke neue Zeile, wenn der Fortschritt abgeschlossen ist
    if iteration == total:
        print()


