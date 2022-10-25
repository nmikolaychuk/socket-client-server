import socket
import signal

from defaults import *
from helpers import print_message, input_message, signal_handler


def udp_client_start():
    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.)

    try:
        while True:
            try:
                # Получение сообщения по UDP
                sock.settimeout(1.)
                data, addr = sock.recvfrom(1024)
            except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, TimeoutError):
                pass
            else:
                # Декодирование сообщения
                data = data.decode()
                if data:
                    print_message(f"Получено сообщение {addr[1]}: {data}")
            try:
                # Формирование ответного сообщения
                mes, is_ok = input_message("Введите сообщение для отправления")

                if mes:
                    # Отправка UDP сообщения
                    sock.sendto(mes.encode(), (HOST_NAME, UDP_PORT))
            except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, TimeoutError):
                pass
    except KeyboardInterrupt:
        sock.close()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    udp_client_start()


if __name__ == "__main__":
    main()
