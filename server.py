import socket

from defaults import *
from helpers import print_message, input_message


def tcp_server_start():
    # Получение адреса сервера
    host = socket.gethostbyname(socket.gethostname())
    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Привязка сокета
    sock.bind((host, PORT))
    sock.listen(1)

    # Ожидание подключения
    print_message("Сервер ожидает подключения клиента...")
    conn, addr = sock.accept()
    print_message(f"Установлено соединение с клиентом {addr[1]}...")

    # Приём и передача сообщений
    while True:
        # Ожидание клиентов при неожиданном отключении последних
        if conn is None and addr is None:
            conn, addr = sock.accept()
            print_message(f"Установлено соединение с клиентом {addr[1]}...")

        try:
            # Ожидание сообщения от клиента
            data = conn.recv(1024)

            # Декодирование сообщения
            data = data.decode()

            if not data:
                raise ConnectionError

            print_message(f"Получено сообщение от клиента {addr[1]}: {data}")
            mes, is_ok = input_message("Введите ответ для клиента")
            if not is_ok:
                break

            # Отправка сообщения
            conn.send(mes.encode())
        except (ConnectionResetError, ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
            print_message("Произошёл непредвиденный разрыв соединения с клиентом. "
                          "Ожидается новое подключение клиента...")
            # Ожидание новых клиентов
            conn.close()
            conn, addr = None, None
            continue

    conn.close()
    sock.close()


def main():
    try:
        tcp_server_start()
    except KeyboardInterrupt:
        print_message("Исполнение программы остановлено пользователем...")


if __name__ == "__main__":
    main()
