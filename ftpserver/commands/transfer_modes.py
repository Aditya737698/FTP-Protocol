import socket

class PortCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "530 Not logged in\r\n"
        if not args:
            return "501 Syntax error\r\n"
        try:
            parts = args[0].split(',')
            ip = '.'.join(parts[:4])
            port = (int(parts[4]) << 8) + int(parts[5])
            session.data_channel.set_active(ip, port)
            return "200 PORT command successful\r\n"
        except:
            return "501 Invalid PORT format\r\n"

class PasvCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "530 Not logged in\r\n"
        ip, port = session.data_channel.set_passive()
        ip_str = ip.replace('.', ',')
        p1, p2 = port >> 8, port & 0xFF
        return f"227 Entering Passive Mode ({ip_str},{p1},{p2})\r\n"