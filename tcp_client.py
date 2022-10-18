import socket
import signal
import sys
import time

from defaults import *
from helpers import print_message, input_message, signal_handler


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
            print_message(f"Установлено соединение с сервером {host}:{port}. Ожидание ответа...")
            break
        time.sleep(1)

    return sock, is_recon_true


def input_and_send(sock):
    # Формирование нового сообщения для клиента
    mes, is_ok = input_message("Введите сообщение для сервера")
    if not is_ok:
        sock.close()
        exit(0)
    sock.send(mes.encode())


def tcp_client_start():
    # Получение адреса сервера
    host, port = sys.argv[1], int(sys.argv[2])

    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Подключение к серверу
    is_connect = try_connect(sock, host, port)

    # Если возникла ошибка при подключении - выход
    if not is_connect:
        return

    print_message(f"Установлено соединение с сервером {host}:{port}...")
    # Отправка первого сообщения
    input_and_send(sock)

    while True:
        # Отправка сообщения серверу
        try:
            sock.settimeout(1)
            data = sock.recv(1024)

            if not data:
                raise ConnectionError()
        except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError):
            print_message("Произошёл разрыв установленного соединения. Сообщение не доставлено...")
            # Попытка переподключения
            sock, is_recon_true = reconnect(sock, host, port)
            # Если переподключение выполнено успешно - продолжение взаимодействия
            if is_recon_true:
                input_and_send(sock)
                continue
            break
        except TimeoutError:
            continue

        # Декодирование сообщения
        data = data.decode()
        print_message(f"Получен ответ от сервера {host}:{port}: {data}")
        input_and_send(sock)

    sock.close()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    tcp_client_start()


if __name__ == "__main__":
    main()
