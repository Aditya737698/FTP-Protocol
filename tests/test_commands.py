import os
import shutil
import pytest
from ftpserver.core.session import FTPSession
from ftpserver.core.command_dispatcher import CommandDispatcher

# Test user credentials (must exist in config/users.txt)
USERNAME = 'alice'
PASSWORD = '1234'

# Test jail root
JAIL_ROOT = os.path.abspath('server_files/users')

@pytest.fixture(autouse=True)
def clean_jail():
    # Clean up test jail before each test
    for root, dirs, files in os.walk(JAIL_ROOT, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            if name != 'mydir':  # preserve mydir for some tests
                shutil.rmtree(os.path.join(root, name), ignore_errors=True)
    yield
    # Clean up after test
    for root, dirs, files in os.walk(JAIL_ROOT, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            if name != 'mydir':
                shutil.rmtree(os.path.join(root, name), ignore_errors=True)

def login(dispatcher):
    assert dispatcher.dispatch(f'USER {USERNAME}') == 'user accepted'
    assert dispatcher.dispatch(f'PASS {PASSWORD}') == 'user logged in'

def test_help():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    out = dispatcher.dispatch('HELP')
    assert 'Available commands' in out

def test_login_logout():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    assert dispatcher.dispatch(f'USER {USERNAME}') == 'user accepted'
    assert dispatcher.dispatch(f'PASS {PASSWORD}') == 'user logged in'
    assert dispatcher.dispatch('QUIT') == 'goodbye'

def test_pwd():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    assert dispatcher.dispatch('PWD') == '/'

def test_mkdir_rmdir():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    assert dispatcher.dispatch('MKDIR testdir') == 'directory created'
    assert os.path.isdir(os.path.join(JAIL_ROOT, 'testdir'))
    assert dispatcher.dispatch('RMDIR testdir') == 'directory removed'
    assert not os.path.exists(os.path.join(JAIL_ROOT, 'testdir'))

def test_cd():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('MKDIR testdir')
    assert dispatcher.dispatch('CD testdir') == 'directory changed'
    assert dispatcher.dispatch('PWD') == '/testdir'

def test_ls():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('TOUCH file1.txt')
    dispatcher.dispatch('TOUCH file2.txt')
    out = dispatcher.dispatch('LS')
    assert 'file1.txt' in out and 'file2.txt' in out

def test_ls_l():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('TOUCH file1.txt')
    out = dispatcher.dispatch('LS-L')
    assert 'file1.txt' in out

def test_rm():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('TOUCH file1.txt')
    assert dispatcher.dispatch('RM file1.txt') == 'file removed'
    assert not os.path.exists(os.path.join(JAIL_ROOT, 'file1.txt'))

def test_rm_r():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('MKDIR dir1')
    dispatcher.dispatch('TOUCH dir1/file.txt')
    assert dispatcher.dispatch('RM-R dir1') == 'directory and contents removed'
    assert not os.path.exists(os.path.join(JAIL_ROOT, 'dir1'))

def test_cp_mv():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('TOUCH file1.txt')
    assert dispatcher.dispatch('CP file1.txt file2.txt') == 'file copied'
    assert os.path.exists(os.path.join(JAIL_ROOT, 'file2.txt'))
    assert dispatcher.dispatch('MV file2.txt file3.txt') == 'file moved'
    assert os.path.exists(os.path.join(JAIL_ROOT, 'file3.txt'))

def test_touch():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    assert dispatcher.dispatch('TOUCH newfile.txt') == 'file touched'
    assert os.path.exists(os.path.join(JAIL_ROOT, 'newfile.txt'))

def test_echo_stdout():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    out = dispatcher.dispatch('ECHO hello world')
    assert out == 'hello world'

def test_echo_to_file():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    assert dispatcher.dispatch('ECHO "hello file" > echo.txt') == 'echoed to file'
    with open(os.path.join(JAIL_ROOT, 'echo.txt')) as f:
        assert f.read() == 'hello file'

def test_cat():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('ECHO "cat content" > catfile.txt')
    out = dispatcher.dispatch('CAT catfile.txt')
    assert 'cat content' in out

def test_stat():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    dispatcher.dispatch('TOUCH statfile.txt')
    out = dispatcher.dispatch('STAT statfile.txt')
    assert 'File:' in out and 'statfile.txt' in out

def test_errors():
    session = FTPSession()
    dispatcher = CommandDispatcher(session)
    login(dispatcher)
    assert 'missing operand' in dispatcher.dispatch('RM')
    assert 'No such file or directory' in dispatcher.dispatch('RM nofile.txt')
    assert 'missing file operand' in dispatcher.dispatch('CP')
    assert 'missing file operand' in dispatcher.dispatch('MV')
    assert 'missing operand' in dispatcher.dispatch('MKDIR')
    assert 'missing operand' in dispatcher.dispatch('RMDIR')
    assert 'missing file operand' in dispatcher.dispatch('TOUCH')
    assert 'missing arguments' in dispatcher.dispatch('ECHO')
    assert 'login required' in CommandDispatcher(FTPSession()).dispatch('LS')