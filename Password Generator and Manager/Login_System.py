from sys import exit
import json
import os
from cryptography.fernet import Fernet

def login_system():
    global login_username

    if not os.path.isfile('database.json'):
        with open('database.json', 'w') as f:
            f.write('{"usernames": [], "passwords": []}')

    with open('database.json', 'r') as f:
        data = json.load(f)
        available_accounts_usernames = data['usernames']
        available_accounts_passwords = data['passwords']
        
    login_signup = input('Do you want to log in or sign up? (log in/sign up) ')

    content_usernames = available_accounts_usernames
    content_passwords = available_accounts_passwords

    login_username = ''
    login_password = ''

    signup_username = ''
    signup_password = ''
    signup_confirm_password = ''

    if login_signup.lower() in ('login', 'log in'):
        login_username = input('Please enter your username: ')
        login_password = input('Please enter your password: ')

        if login_username in (available_accounts_usernames):
            key = make_key(login_username)
            fer = Fernet(key)

            if login_password == str(fer.decrypt(available_accounts_passwords[available_accounts_usernames.index(login_username)].encode()).decode()):
                print('Access Granted')
                return [True, login_username]

            else:
                print("Access Denied")
                k = input("\nPress enter to close program ")
                exit()             

        else:
            print("Access Denied")
            k = input("\nPress enter to close program ")
            exit()

    elif login_signup.lower() in ('sign up', 'signup'):
        signup_username = input('Please enter a username. This username will be asked if you want to login: ')

        if signup_username in available_accounts_usernames:
            print("This username is already taken.")
            k = input("\nPress enter to close program ")
            exit()

        signup_password = input('Please enter a password. You will be asked to confirm your password: ')
        if len(signup_password) < 8:
            print('This password should be more than 8 characters. Please enter your info again.')
            k = input("\nPress enter to close program ")
            exit()

        signup_confirm_password = input('Please confirm your password: ')
        if signup_password == signup_confirm_password:

            key = make_key(signup_username)
            fer = Fernet(key)

            available_accounts_usernames.append(signup_username)
            available_accounts_passwords.append(str(fer.encrypt(signup_password.encode()).decode())) 

            print('Your account has been created. Log back in to access it.')

            content_usernames = available_accounts_usernames
            content_passwords = available_accounts_passwords

            with open('database.json', 'w') as f:
                json.dump({'usernames': content_usernames, 'passwords': content_passwords}, f)

            k = input("\nPress enter to close program ")
            exit()
            
        else:
            print("These passwords don't match. Please enter your info again")
            k = input("\nPress enter to close program ")
            exit()

    else:
        print("Please choose one of the two.")
        k = input("\nPress enter to close program ")
        exit()

def make_key(username):
    if not os.path.isfile(f"Keys\Account Password\{username}.key"):
        key = Fernet.generate_key()
        with open(f"Keys\Account Password\{username}.key", "wb") as key_file:
            key_file.write(key)

        return key

    else:
        file = open(f"Keys\Account Password\{username}.key", "rb")
        key = file.read()
        file.close()
        
        return key