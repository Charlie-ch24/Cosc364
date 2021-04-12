import socket, select
LocalHost = "127.0.0.1"


def create(input_ports):

    binded_sockets = []
    for input in input_ports:
        input_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        input_socket.bind((LocalHost, input))
        binded_sockets.append(input_socket)

    return binded_sockets