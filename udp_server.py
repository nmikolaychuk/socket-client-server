import socket
import signal

from defaults import *
from helpers import print_message, input_message, signal_handler


def udp_server_start():
    # Получение адреса сервера
    host = socket.gethostbyname(socket.gethostname())
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, UDP_PORT))

    print_message("Сервер успешно запущен. Ожидаются UDP-сообщения...")
    addr = None

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

            if addr is not None:
                try:
                    # Формирование ответного сообщения
                    mes, is_ok = input_message("Введите сообщение для отправления")
                    if mes:
                        # Отправка UDP сообщения
                        sock.sendto(mes.encode(), addr)
                except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError,
                        ConnectionResetError, TimeoutError, TypeError):
                    pass
    except KeyboardInterrupt:
        sock.close()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    udp_server_start()


if __name__ == "__main__":
    main()
