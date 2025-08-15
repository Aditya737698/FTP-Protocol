import socket
import threading
from ftpserver.core.client_handler import ClientHandler
from ftpserver.utils.logger import logger

class FTPServer:
    def __init__(self, host='0.0.0.0', port=21):
        self.host = host
        self.port = port

    def start(self):
        logger.info(f"Starting FTP Server on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            logger.info("Server is listening for connections...")

            while True:
                client_sock, addr = server_socket.accept()
                logger.info(f"Connection from {addr}")
                handler = ClientHandler(client_sock, addr)
                handler.start()
