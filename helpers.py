import datetime


def print_message(text: str):
    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    print("[" + str(now) + "] " + text)


def input_message(print_mes: str):
    is_ok = True
    mes = ""
    try:
        while not mes:
            mes = input(print_mes + " -> ")
    except KeyboardInterrupt:
        print_message("Выполнение программы принудительно остановлено пользователем...")
        is_ok = False

    return mes, is_ok
