import socket
import signal
import sys

from helpers import print_message, input_message, signal_handler


def create_socket(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    return sock


def tcp_server_start():
    # Получение адреса сервера
    host, port = None, None
    try:
        host, port = sys.argv[1], int(sys.argv[2])
    except IndexError:
        print("Не указаны следующие аргументы: 1) адрес подключения; 2) порт подключения.")
        exit(-1)

    # Создание сокета
    sock = create_socket(host, port)

    # Ожидание подключения
    print_message("Сервер ожидает подключения клиента...")
    conn, addr = None, None

    # Приём и передача сообщений
    try:
        while True:
            # Ожидание клиентов при неожиданном отключении последних
            if conn is None and addr is None:
                try:
                    sock.settimeout(1)
                    conn, addr = sock.accept()
                except TimeoutError:
                    continue

                print_message(f"Установлено соединение с клиентом {addr[0]}:{port} ({addr[1]})...")

            try:
                # Ожидание сообщения от клиента
                conn.settimeout(1)
                data = conn.recv(1024)

                if not data:
                    raise ConnectionError

                # Декодирование сообщения
                data = data.decode()
                if not data.strip():
                    continue

                print_message(f"Получено сообщение от клиента {addr[0]}:{port} ({addr[1]}): {data.lstrip()}")
                mes, is_ok = input_message("Введите ответ для клиента")
                if not is_ok:
                    break

                # Отправка сообщения
                conn.settimeout(1)
                conn.send(mes.encode())
            except TimeoutError:
                if sock.getsockname()[0] == socket.gethostbyname(socket.gethostname()):
                    try:
                        sock.settimeout(1)
                        conn1, addr1 = sock.accept()
                    except TimeoutError:
                        continue
                    else:
                        conn.close()
                        conn, addr = conn1, addr1
                        print_message("Ожидание сообщения от клиента.")
                        continue
                else:
                    print_message("Произошёл непредвиденный разрыв соединения с клиентом. "
                                  "Ожидается новое подключение клиента...")
                    # Ожидание новых клиентов
                    conn.close()
                    conn, addr = None, None

                    # Пересоздание сокета
                    sock.close()
                    del sock
                    sock = create_socket(host, port)
                    continue
            except (ConnectionResetError, ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                print_message("Произошёл непредвиденный разрыв соединения с клиентом. "
                              "Ожидается новое подключение клиента...")
                # Ожидание новых клиентов
                conn.close()
                conn, addr = None, None

                # Пересоздание сокета
                sock.close()
                del sock
                sock = create_socket(host, port)
                continue
    except KeyboardInterrupt:
        conn.close()
        sock.close()
    else:
        conn.close()
        sock.close()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    tcp_server_start()


if __name__ == "__main__":
    main()
