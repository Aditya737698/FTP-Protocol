from ftpserver.core.data_channel import DataChannel

class FTPSession:
    def __init__(self):
        self.username = None
        self.logged_in = False
        self.cwd = "/"
        self.transfer_type = "A"
        self.data_channel = DataChannel()
        self._user_db = {}  # Add this line