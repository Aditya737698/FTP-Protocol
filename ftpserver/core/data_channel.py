import socket

class DataChannel:
    def __init__(self):
        self.mode = None
        self.data_socket = None
        self.client_addr = None  # (host, port)

    def set_active(self, host, port):
        self.mode = "ACTIVE"
        self.client_addr = (host, port)

    def set_passive(self):
        self.mode = "PASSIVE"
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.bind(('', 0))  # Bind to random port
        self.data_socket.listen(1)
        ip, port = self.data_socket.getsockname()
        return ip, port

    def open(self):
        if self.mode == "ACTIVE":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.client_addr)
            return sock
        elif self.mode == "PASSIVE":
            conn, _ = self.data_socket.accept()
            return conn
        else:
            raise Exception("Data connection mode not set")

    def close(self):
        if self.data_socket:
            self.data_socket.close()
            self.data_socket = None
        self.client_addr = None
        self.mode = None
