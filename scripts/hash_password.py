import bcrypt
import sys

if len(sys.argv) != 2:
    print("Usage: python hash_password.py <password>")
    sys.exit(1)

password = sys.argv[1]
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hash.decode()) 