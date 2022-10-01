import socket

from defaults import *
from helpers import print_message, input_message


def try_connect(sock, host, port):
    # Обработка подключения
    try:
        sock.connect((host, port))
    except TimeoutError:
        print_message(FAIL_POSTSCRIPT_CONNECT + "т.к. не был получен нужный отклик за требуемое время...")
        return False
    except socket.gaierror:
        print_message(FAIL_POSTSCRIPT_CONNECT + "т.к. был введен некорректный сетевой адрес...")
        return False
    except ConnectionRefusedError:
        print_message(FAIL_POSTSCRIPT_CONNECT + "т.к. конечный компьютер отверг запрос на подключение...")
        return False
    except OSError:
        print_message(FAIL_POSTSCRIPT_CONNECT + "т.к. сделан запрос на подключение для уже подключенного сокета...")
        return False

    return True


def reconnect(sock, host, port):
    # Осуществление попыток переподключения
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_recon_true = False
    for i in range(RECONNECT_TRY_COUNT):
        print_message(f"Попытка переподключения ({i}/{RECONNECT_TRY_COUNT})...")
        is_connect = try_connect(sock, host, port)
        if is_connect:
            is_recon_true = True
            print_message(f"Установлено соединение с сервером {host}:{PORT}. Ожидание ответа...")
            break

    return sock, is_recon_true


def tcp_client_start():
    # Получение адреса для подключения
    host, is_ok = input_message("Введите адрес сервера для подключения (IPv4)")
    if not is_ok:
        return

    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Подключение к серверу
    is_connect = try_connect(sock, host, PORT)

    # Если возникла ошибка при подключении - выход
    if not is_connect:
        return

    print_message(f"Установлено соединение с сервером {host}:{PORT}...")

    mes, is_ok = input_message("Введите сообщение для сервера")
    if not is_ok:
        sock.close()
        return

    while True:
        # Отправка сообщения серверу
        try:
            sock.send(mes.encode())
            data = sock.recv(1024)
        except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, TimeoutError):
            print_message("Произошёл разрыв установленного соединения...")
            # Попытка переподключения
            sock, is_recon_true = reconnect(sock, host, PORT)
            # Если переподключение выполнено успешно - продолжение взаимодействия
            if is_recon_true:
                continue
            break

        # Декодирование сообщения
        data = data.decode()

        print_message(f"Получен ответ от сервера {host}:{PORT}: {data}")

        # Формирование нового сообщения для клиента
        mes, is_ok = input_message("Введите сообщение для сервера")
        if not is_ok:
            break

    sock.close()


def main():
    try:
        tcp_client_start()
    except KeyboardInterrupt:
        print_message("Исполнение программы остановлено пользователем...")


if __name__ == "__main__":
    main()
