# 🛰️ Custom FTP Server (RFC 959 Compliant)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A modular, object-oriented implementation of the FTP protocol in Python. This project is designed for educational purposes and demonstrates a custom FTP server with user authentication, role-based access control (RBAC), and a wide range of custom FTP commands. The server supports both active (PORT) and passive (PASV) data transfer modes and closely follows [RFC 959](https://datatracker.ietf.org/doc/html/rfc959).

---

## Features
- **RFC 959 Compliant**: Implements standard FTP protocol features.
- **Active & Passive Modes**: Supports both PORT (active) and PASV (passive) data connections.
- **User Authentication**: Secure login with bcrypt-hashed passwords.
- **Role-Based Access Control**: Admin and user roles, with fine-grained command permissions.
- **Extensive Command Set**: Includes all basic and several advanced FTP commands.
- **Modular Design**: Clean, object-oriented codebase for easy extension and maintenance.

## Project Structure
```
Custom-FTP-Protocol/
├── ftpserver/           # Main server implementation
│   ├── commands/       # FTP command handlers
│   ├── config/         # User and server configuration
│   ├── core/           # Core server logic (session, dispatcher, server)
│   └── utils/          # Utility functions
├── server_files/       # User file storage (jail)
├── scripts/            # Startup scripts
├── tests/              # Pytest-based test suite
├── requirements.txt    # Python dependencies
├── setup.py            # Packaging info
└── README.md           # Project documentation
```

## Setup & Installation
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd Custom-FTP-Protocol
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the server:**
   ```sh
   python scripts/ftpserver
   ```
   The server listens on port **2121** by default.

4. **Use telnet or netcat to communicate with the server:**
   ```sh
   telnet 127.0.0.1 2121
   ```

   ```sh
   nc 127.0.0.1 2121
   ```

## Configuration
- **User Accounts:**
  - Users are defined in `ftpserver/config/users.json` with fields: `username`, `password` (bcrypt hash), `role` (admin/user), and `permissions`.
  - Example:
    ```json
    {
      "username": "admin",
      "password": "<bcrypt-hash>",
      "role": "admin",
      "permissions": []
    }
    ```
- **Default admin credentials:**
  - ```
    USER: admin
    PASS: 123
    ```
- **File Storage:**
  - Each user is jailed to their directory under `server_files/users/`.

## Implemented FTP Commands
| Command      | Description                                      |
|--------------|--------------------------------------------------|
| USER         | Login with username                              |
| PASS         | Login with password                              |
| QUIT         | Close the connection                             |
| NOOP         | No operation                                     |
| HELP         | Show help message                                |
| PWD          | Print working directory                          |
| CD           | Change directory                                 |
| LS           | List directory contents                          |
| LS-L         | Long listing of directory contents               |
| NLST         | Name list of directory                           |
| MKDIR        | Make directory                                   |
| RMDIR        | Remove empty directory                           |
| RM           | Remove file                                      |
| RM-R         | Remove directory and contents recursively        |
| CP           | Copy file or directory                           |
| MV           | Move or rename file or directory                 |
| RETR         | Retrieve (download) file                         |
| STOR         | Store (upload) file                              |
| CAT          | Display file contents                            |
| STAT         | Show file or directory statistics                |
| TOUCH        | Create or update file timestamp                  |
| ECHO         | Echo text to output or write to file             |
| PORT         | Set active mode for data transfer                |
| PASV         | Set passive mode for data transfer               |
| ADDUSER      | (Admin) Add a new user                           |
| DELUSER      | (Admin) Delete a user                            |
| SETROLE      | (Admin) Set a user's role                        |
| GRANT        | (Admin) Grant a user permission for a command    |
| REVOKE       | (Admin) Revoke a user's command permission       |

## Example Usage
- **Login:**
  ```
  USER admin
  PASS 123
  ```
- **List files:**
  ```
  LS
  ```
- **Upload a file:**
  ```
  STOR myfile.txt
  ```
- **Download a file:**
  ```
  RETR myfile.txt
  ```
- **Admin: Add a user:**
  ```
  ADDUSER name password role
  ```

## Testing
- Run all tests using pytest:
  ```sh
  pytest tests/test_commands.py
  ```
- Tests cover all major commands and error cases (see `tests/test_commands.py`).

## Notes
- Default port is **2121** (changeable in `scripts/ftpserver`).
- Only users listed in `users.json` can log in.
- Admin users can manage other users and permissions.
- All file operations are sandboxed to `server_files/users/`.

## License
This project is for educational use as a college project.

