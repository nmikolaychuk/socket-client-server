import datetime
import sys
import msvcrt
import time


def signal_handler(sig, frame):
    print('Выполнение программы прервано пользователем!')
    raise KeyboardInterrupt


def print_message(text: str):
    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    print("[" + str(now) + "] " + text)


def input_message(print_mes: str):
    starttime = time.time()
    mes = ""
    while time.time() - starttime < 1:
        if msvcrt.kbhit():
            mes = input(print_mes + " -> ")
            break

    is_ok = True
    if not mes:
        is_ok = False

    return mes, is_ok
