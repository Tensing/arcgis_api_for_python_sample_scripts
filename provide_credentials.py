import json, os
from getpass import getpass #to accept passwords in an interactive fashion

def provide_credentials():
    file_with_credentials = 'my_credentials.json'
    username = ''
    password = ''
    if os.path.exists(file_with_credentials):
        with open(file_with_credentials) as f:
            data = json.load(f)
            username = data['username']
            password = data['password']
    if not username or username == 'USERNAME' or not password or password == 'PASSWORD':
        username = input('Please enter your username: ')
        password = getpass('Please enter your password (this will remain invisible): ')
    return username, password