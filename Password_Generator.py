import secrets
import sys

class GeneratePassword:

    def __init__(self, length, have_numbers="yes", have_uppercase="yes", have_specialcharacters="yes"):
        self.length = length
        self.have_numbers = have_numbers
        self.have_uppercase = have_uppercase
        self.have_specialcharacters = have_specialcharacters

        self.lowercase = "abcdefghijklmnopqrstuvwxyz"
        self.numbers = "1234567890"
        self.uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.specialcharacters = "[$&+,:;=?@#|'<>.-^*()%!]"

        self.charset = [self.lowercase]
        self.password = []

    def make_password(self):
        if self.have_numbers == "yes":
            self.charset.append(self.numbers)
        if self.have_uppercase == "yes":
            self.charset.append(self.uppercase)
        if self.have_specialcharacters == "yes":
            self.charset.append(self.specialcharacters)

        for i in range(0, self.length):
            character_type = secrets.choice(self.charset)
            character = secrets.choice(character_type)
            self.password.append(character)

        self.password = "".join(self.password)
        return self.password

def ask_password():
    try:
        length = int(input("What is the length of the password? "))
    except:
        print("Type a number")
        k = input("\nPress enter to close program ")

        sys.exit()
        
    have_numbers = input("Do you want numbers? (yes/no) ")
    have_uppercase = input("Do you want uppercase characters? (yes/no) ")
    have_specialcharacters = input("Do you want special characters? (yes/no) ")

    generated_password = GeneratePassword(length, have_numbers, have_uppercase, have_specialcharacters)
    return generated_password.make_password()