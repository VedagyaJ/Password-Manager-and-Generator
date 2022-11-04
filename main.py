from Login_System import *
from Password_Generator import *
import json
import os
from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        try:
            if not os.path.isfile(f"Passwords\{login_attempt[1]}.json"):
                with open(f"Passwords\{login_attempt[1]}.json", "w") as f:
                    f.write('{"websites": [], "passwords": []}')
        except IndexError:
            pass

        try:
            with open(f"Passwords\{login_attempt[1]}.json", "r") as f:
                data = json.load(f)
                self.account_passwords = data["passwords"]
                self.account_websites = data["websites"]
        except IndexError:
            pass

        try:
            self.key = self.make_key()
            self.fer = Fernet(self.key)

        except IndexError:
            pass

    def make_key(self):
        if not os.path.isfile(f"Keys\Account Keys\{login_attempt[1]}.key"):
            key = Fernet.generate_key()
            with open(f"Keys\Account Keys\{login_attempt[1]}.key", "wb") as key_file:
                key_file.write(key)

            return key

        else:
            file = open(f"Keys\Account Keys\{login_attempt[1]}.key", "rb")
            key = file.read()
            file.close()
            return key

    def store_password(self, my_password, website):
        with open(f"Passwords\{login_attempt[1]}.json", "w") as f:
            self.account_passwords.append(my_password)
            self.account_websites.append(website)
            json.dump({"websites": self.account_websites, "passwords": self.account_passwords}, f)

    def add_password(self):
        my_password = ask_password()
        website = input("Which website do you want this password to be associated to? ")
        print(f"Password: {my_password}")
        print("Password successfully added to account.")
        self.store_password(str(self.fer.encrypt(my_password.encode()).decode()), website.lower())
        k = input("\nPress enter to close program ")

    def show_passwords(self):
        choice2 = input("Would you like to view a password for a specific website or would you like to view all your passwords? (specific website/all passwords): ")
        if choice2.lower() == "specific website":
            website_wanted = input("Which website? ")
            if website_wanted.lower() in self.account_websites:
                print(f"Password: {str(self.fer.decrypt(self.account_passwords[self.account_websites.index(website_wanted.lower())].encode()).decode())}")
                k = input("\nPress enter to close program ")
            else:
                print("You have not saved a password for this website.")
                k = input("\nPress enter to close program ")

        elif choice2.lower() == "all passwords":
            for i in range(0, len(self.account_passwords)):
                print(f"{self.account_websites[i]:15}:      {str(self.fer.decrypt(self.account_passwords[i].encode()).decode())}")
            k = input("\nPress enter to close program ")

        else:
            print("Please choose one of the two")
            k = input("\nPress enter to close program ")

login_attempt = login_system()
password_manager = PasswordManager()

if True in login_attempt:
    choice = input("Would you like to generate a new password or view existing passwords? (generate/view): ")
    
    if choice.lower() == "generate":
        password_manager.add_password()

    elif choice.lower() == "view":
        password_manager.show_passwords()

    else:
        print("Please choose one of the two")