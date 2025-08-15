from ftpserver.core.session import FTPSession
from ftpserver.core.command_dispatcher import CommandDispatcher
from ftpserver.core.session import FTPSession
from ftpserver.core.command_dispatcher import CommandDispatcher
import threading

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.session = FTPSession()
        self.dispatcher = CommandDispatcher(self.session)

    def run(self):
        try:
            self.client_socket.sendall(b"220 Welcome to FTPServer\r\n")
            while True:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                response = self.dispatcher.dispatch(data)
                self.client_socket.sendall(response.encode())
                if response.startswith("221"):
                    break
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            self.client_socket.close()
