import sys
import time

def loading():
    loading = "\\-/|\\"
    print("in progress", end=' ')
    while True:
        for L in loading:
            print(f'\b{L}', end='')  # Use \b to move the cursor one position to the left and print the spinner character
            sys.stdout.flush()       # Flush the output buffer to make sure the character is printed immediately
            time.sleep(0.07) 

loading() 
