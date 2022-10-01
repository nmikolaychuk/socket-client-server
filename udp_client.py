import socket

from defaults import *
from helpers import print_message, input_message


def udp_client_start():
    # Получение адреса для подключения
    host, is_ok = input_message("Введите адрес сервера для подключения (IPv4)")
    if not is_ok:
        return

    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.)

    mes, is_ok = input_message("Введите сообщение для сервера")
    if not is_ok:
        sock.close()
        return

    while True:
        try:
            # Отправка сообщения серверу
            sock.sendto(mes.encode(), (host, PORT))
            # Получение ответного сообщения
            data, addr = sock.recvfrom(1024)

            # Декодирование ответного сообщения
            data = data.decode()

            print_message(f"Получен ответ от {addr[0]}:{addr[1]}: {data}")

            # Формирование нового сообщения для клиента
            mes, is_ok = input_message("Введите сообщение для сервера")
            if not is_ok:
                break
        except TimeoutError:
            pass

    sock.close()


def main():
    try:
        udp_client_start()
    except KeyboardInterrupt:
        print_message("Исполнение программы остановлено пользователем...")


if __name__ == "__main__":
    main()
