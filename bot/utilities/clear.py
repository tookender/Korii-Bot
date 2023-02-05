import os


def clear():
    if os.name == "nt":
        return os.system("cls")
        
    os.system("clear")