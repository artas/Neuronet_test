import time
import wave
import sys
from socket import socket, AF_INET, SOCK_DGRAM

host = '127.0.0.1'
port = 9999
connection_params = (host, port)


def read_and_send_wave_file(filename):
    """
    :param filename: Название файла, который надо передать
    """
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.sendto(b'Accept', connection_params)
    try:
        w = wave.open(filename, 'rb')
        data = w.readframes(4096)
        while data:

            if udp_socket.sendto(data, connection_params):
                data = w.readframes(4096)
                time.sleep(1/1000)
        w.close()
        udp_socket.sendto(b'Close', connection_params)
    except FileNotFoundError:
        print(f"Ошибка! Фаил: {filename} не найден")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        read_and_send_wave_file(sys.argv[1])
    else:
        print('Необходимо в качестве 2го аргумента передать название файла')
        print('Например вот так "python client.py tts.wav" ')
