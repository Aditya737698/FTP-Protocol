class NoopCommand:
    def handle(self, args, session):
        return "200 NOOP command successful.\r\n"

class HelpCommand:
    def handle(self, args, session):
        help_text = (
            "Available commands:\r\n"
            "USER <username>         - Login with username\r\n"
            "PASS <password>         - Login with password\r\n"
            "QUIT                    - Close the connection\r\n"
            "NOOP                    - No operation\r\n"
            "PWD                     - Print working directory\r\n"
            "CD <dir>                - Change directory\r\n"
            "LS [dir]                - List directory contents\r\n"
            "LS-L [dir]              - Long listing of directory contents\r\n"
            "NLST [dir]              - Name list of directory\r\n"
            "MKDIR <dir>             - Make directory\r\n"
            "RMDIR <dir>             - Remove empty directory\r\n"
            "RM <file>               - Remove file\r\n"
            "RM-R <dir>              - Remove directory and contents recursively\r\n"
            "CP <src> <dst>          - Copy file or directory\r\n"
            "MV <src> <dst>          - Move or rename file or directory\r\n"
            "RETR <file>             - Retrieve (download) file\r\n"
            "STOR <file>             - Store (upload) file\r\n"
            "CAT <file>              - Display file contents\r\n"
            "STAT <file|dir>         - Show file or directory statistics\r\n"
            "TOUCH <file>            - Create or update file timestamp\r\n"
            "ECHO <text>             - Echo text to output\r\n"
            "ECHO <text> > <file>    - Write text to file\r\n"
            "HELP                    - Show this help message\r\n"
            "End of HELP\r\n"
        )
        return help_text