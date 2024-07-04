import sys
import time

def loading(stop_event):
    loading_chars = "\\-/|\\"
    print("in progress", end=' ')
    while not stop_event.is_set():
        for L in loading_chars:
            if stop_event.is_set():
                break
            print(f'\b{L}', end='', flush=True)
            time.sleep(0.07)