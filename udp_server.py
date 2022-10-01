import socket

from defaults import *
from helpers import print_message, input_message


def udp_server_start():
    # Получение адреса сервера
    host = socket.gethostbyname(socket.gethostname())
    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Привязка сокета
    sock.bind((host, PORT))

    print_message("Сервер успешно запущен. Ожидаются UDP-сообщения...")

    while True:
        try:
            # Получение сообщения от клиента по UDP
            data, addr = sock.recvfrom(1024)
            # Декодирование сообщения
            data = data.decode()
        except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, TimeoutError):
            print_message(f"Не удалось отправить сообщение. Произошёл разрыв соединения...")
            continue

        print_message(f"Получено сообщение от клиента {addr[1]}: {data}")

        # Формирование ответного сообщения
        mes, is_ok = input_message("Введите ответ для клиента")
        if not is_ok:
            break

        # Отправка UDP сообщения
        sock.sendto(mes.encode(), addr)

    sock.close()


def main():
    try:
        udp_server_start()
    except KeyboardInterrupt:
        print_message("Исполнение программы остановлено пользователем...")


if __name__ == "__main__":
    main()
