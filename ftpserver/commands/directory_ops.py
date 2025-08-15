import os
import shutil
from ftpserver.utils.filesystem import resolve_path, list_dir, change_directory
import errno

class PwdCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        return session.cwd + "\n"

class CwdCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        if not args:
            return "cd: missing operand\n"
        try:
            session.cwd = change_directory(session.cwd, args[0])
            return "directory changed\n"
        except NotADirectoryError:
            return f"cd: {args[0]}: Not a directory\n"
        except ValueError:
            return f"cd: {args[0]}: Access denied\n"
        except Exception as e:
            return f"cd: {args[0]}: {e}\n"

class ListCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        try:
            path = resolve_path(session.cwd, args[0] if args else ".")
            files = list_dir(path)
            data = "\n".join(files)
            return data + "\n"
        except Exception as e:
            return f"ls: {e}\n"

class NlstCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        try:
            path = resolve_path(session.cwd, args[0] if args else ".")
            files = list_dir(path)
            data = "\n".join(f for f in files if not f.startswith('.'))
            return data + "\n"
        except Exception as e:
            return f"nlst: {e}\n"

class MkdirCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        if not args:
            return "mkdir: missing operand\n"
        try:
            dir_path = resolve_path(session.cwd, args[0])
            os.makedirs(dir_path, exist_ok=False)
            return "directory created\n"
        except FileExistsError:
            return f"mkdir: cannot create directory '{args[0]}': File exists\n"
        except Exception as e:
            return f"mkdir: cannot create directory '{args[0]}': {e}\n"

class RmdirCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        if not args:
            return "rmdir: missing operand\n"
        try:
            dir_path = resolve_path(session.cwd, args[0])
            os.rmdir(dir_path)
            return "directory removed\n"
        except FileNotFoundError:
            return f"rmdir: failed to remove '{args[0]}': No such file or directory\n"
        except OSError:
            return f"rmdir: failed to remove '{args[0]}': Directory not empty or cannot be removed\n"
        except Exception as e:
            return f"rmdir: failed to remove '{args[0]}': {e}\n"

class RmRecursiveCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        if not args:
            return "rm -r: missing operand\n"
        try:
            dir_path = resolve_path(session.cwd, args[0])
            shutil.rmtree(dir_path)
            return "directory and contents removed\n"
        except FileNotFoundError:
            return f"rm -r: cannot remove '{args[0]}': No such file or directory\n"
        except Exception as e:
            return f"rm -r: cannot remove '{args[0]}': {e}\n"

class LsLongCommand:
    def handle(self, args, session):
        if not session.logged_in:
            return "login required\n"
        import stat, time
        try:
            path = resolve_path(session.cwd, args[0] if args else ".")
            files = os.listdir(path)
            lines = []
            for f in files:
                fp = os.path.join(path, f)
                st = os.stat(fp)
                perms = stat.filemode(st.st_mode)
                nlink = st.st_nlink
                owner = st.st_uid if hasattr(st, 'st_uid') else 0
                group = st.st_gid if hasattr(st, 'st_gid') else 0
                size = st.st_size
                mtime = time.strftime('%b %d %H:%M', time.localtime(st.st_mtime))
                lines.append(f"{perms} {nlink} {owner} {group} {size} {mtime} {f}")
            data = "\n".join(lines)
            return data + "\n"
        except Exception as e:
            return f"ls -l: {e}\n"
