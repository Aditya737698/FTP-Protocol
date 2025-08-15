"""
User Access Control (RBAC)
-------------------------
- All users are stored in users.json with roles and permissions.
- Admins can add/remove users, set roles, and grant/revoke permissions.
- Passwords are hashed using bcrypt.
- Each command checks user permissions before execution.
- Invalid password hashes are logged and skipped.
- When a user enters their password, it is hashed and compared to the stored hash using bcrypt.
"""
import os
import json
import bcrypt
import logging
from ftpserver.utils.filesystem import BASE_DIR

USER_DB_PATH = os.path.join(os.path.dirname(__file__), '../config/users.json')
logger = logging.getLogger("ftpserver.access_control")

# Helper functions for user DB

def is_valid_bcrypt_hash(hash_str):
    try:
        # bcrypt hash must start with $2b$ or $2a$ and be 60 chars
        return (hash_str.startswith("$2b$") or hash_str.startswith("$2a$")) and len(hash_str) == 60
    except Exception:
        return False

def load_users():
    if not os.path.exists(USER_DB_PATH):
        return []
    with open(USER_DB_PATH, 'r') as f:
        data = json.load(f)
        users = []
        for user in data.get('users', []):
            if not is_valid_bcrypt_hash(user.get('password', '')):
                # logger.warning(f"Skipping user {user.get('username', '<unknown>')}: invalid bcrypt hash.")
                continue
            users.append(user)
        return users

def save_users(users):
    with open(USER_DB_PATH, 'w') as f:
        json.dump({'users': users}, f, indent=2)

def find_user(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def check_password(stored_hash, password):
    """
    Compares a plaintext password entered by the user to the stored bcrypt hash.
    The password is hashed and checked using bcrypt's checkpw, which is secure and recommended.
    """
    try:
        # bcrypt.checkpw will hash the input password and compare to the stored hash
        return bcrypt.checkpw(password.encode(), stored_hash.encode())
    except Exception as e:
        logger.error(f"Password check failed: {e}")
        return False

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# RBAC Command Handlers
class UserCommand:
    def handle(self, args, session):
        if not args:
            return "user: missing username"
        session.username = args[0]
        session.logged_in = False
        user = find_user(session.username)
        session.user_obj = user
        session.cwd = "/"  # All users start in the same directory
        if user:
            return "user accepted\n"
        else:
            return "user: unknown user\n"

class PassCommand:
    def handle(self, args, session):
        if not session.username:
            return "pass: login with USER first\n"
        if not args:
            return "pass: missing password\n"
        user = session.user_obj
        try:
            # User enters plaintext password; we compare it to the stored hash using bcrypt
            if user and check_password(user['password'], args[0]):
                session.logged_in = True
                session.role = user['role']
                session.permissions = user.get('permissions', [])
                return f"user logged in as {session.role}\n"
            else:
                session.logged_in = False
                return "pass: incorrect password\n"
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            session.logged_in = False
            return "pass: authentication error\n"

class QuitCommand:
    def handle(self, args, session):
        return "goodbye\n"

# Admin-only commands
class AddUserCommand:
    def handle(self, args, session):
        if not (session.logged_in and session.role == 'admin'):
            return "permission denied\n"
        if len(args) < 3:
            return "adduser: usage: ADDUSER <username> <password> <role>\n"
        username, password, role = args[:3]
        if find_user(username):
            return "adduser: user already exists\n"
        users = load_users()
        users.append({
            'username': username,
            'password': hash_password(password),
            'role': role,
            'permissions': [] if role == 'admin' else ["RETR", "STOR", "LS"]
        })
        save_users(users)
        return f"user {username} added\n"

class DelUserCommand:
    def handle(self, args, session):
        if not (session.logged_in and session.role == 'admin'):
            return "permission denied\n"
        if not args:
            return "deluser: usage: DELUSER <username>\n"
        username = args[0]
        users = load_users()
        users = [u for u in users if u['username'] != username]
        save_users(users)
        return f"user {username} deleted\n"

class SetRoleCommand:
    def handle(self, args, session):
        if not (session.logged_in and session.role == 'admin'):
            return "permission denied\n"
        if len(args) < 2:
            return "setrole: usage: SETROLE <username> <role>\n"
        username, role = args[:2]
        users = load_users()
        for u in users:
            if u['username'] == username:
                u['role'] = role
                save_users(users)
                return f"role for {username} set to {role}\n"
        return "setrole: user not found\n"

# List of valid commands that can be granted/revoked (non-admin commands only)
GRANTABLE_COMMANDS = {
    "NOOP", "PWD", "CD", "LS", "NLST", "PORT", "PASV", "RETR", "STOR", "CAT", "MKDIR", "RMDIR", "RM", "RM-R", "CP", "MV", "LS-L", "STAT", "TOUCH", "ECHO"
}

class GrantCommand:
    def handle(self, args, session):
        if not (session.logged_in and session.role == 'admin'):
            return "permission denied\n"
        if len(args) < 2:
            return "grant: usage: GRANT <username> <command>\n"
        username, command = args[:2]
        command = command.upper()
        if command not in GRANTABLE_COMMANDS:
            return f"grant: invalid command '{command}'. Allowed: {', '.join(sorted(GRANTABLE_COMMANDS))}\n"
        users = load_users()
        for u in users:
            if u['username'] == username:
                if command not in u['permissions']:
                    u['permissions'].append(command)
                    save_users(users)
                return f"granted {command} to {username}\n"
        return "grant: user not found\n"

class RevokeCommand:
    def handle(self, args, session):
        if not (session.logged_in and session.role == 'admin'):
            return "permission denied\n"
        if len(args) < 2:
            return "revoke: usage: REVOKE <username> <command>\n"
        username, command = args[:2]
        command = command.upper()
        if command not in GRANTABLE_COMMANDS:
            return f"revoke: invalid command '{command}'. Allowed: {', '.join(sorted(GRANTABLE_COMMANDS))}\n"
        users = load_users()
        for u in users:
            if u['username'] == username:
                if command in u['permissions']:
                    u['permissions'].remove(command)
                    save_users(users)
                return f"revoked {command} from {username}\n"
        return "revoke: user not found\n"