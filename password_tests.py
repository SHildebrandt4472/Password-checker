from dict import load_word_list, word_exists
import pyhibp
from pyhibp import pwnedpasswords as pw

# Create a class to store the password test information
class PasswordTest:
    def __init__(self, text, func, score, char_count, delayed=False):
        self.text = text
        self.func = func
        self.score = score
        self.icon = None
        self.char_count = char_count
        self.delayed = delayed
        self.disabled = False 

# Define a set of functions to test a given password

# length >= 8 test
def check_length_8(password):
    if len(password) >= 8:
        return True
    else:
        return False

# length >= 13 test
def check_length_13(password):
    if len(password) >= 13:
        return True
    else:
        return False

# Check for upper and lower case letters
def check_case(password):
    upper_count = 0
    lower_count = 0
    for letter in password:
        if letter >= 'A' and letter <= 'Z': # Check for uppercase letters
            upper_count += 1
        elif letter >= 'a' and letter <= 'z': # Check for lowercase letters
            lower_count += 1

    if upper_count >= 1 and lower_count >= 1: # Check if both upper and lower case letters are present
        return True
    else:
        return False

# Check for numbers
def check_num(password):
    for letter in password:
        if letter >= '0' and letter <= '9': # Check for numbers
            return True
    return False

# Check for symbols
def check_symbol(password):
    symbols = "`~!@#$%^&*()_+-=[]{}|;:,.<>?/\\\'\""
    for letter in password:
        if letter in symbols: # Check for symbols
            return True
    return False

# Check if password is based on a dictionary word
def check_dictionary(password):
    if word_exists(password): # Check if password is a dictionary word
        return False
    if len(password) > 3:
        if word_exists(password[0:-1]):  # Check without last character
            return False
        if word_exists(password[1:]):  # Check without first character
            return False
    if len(password) > 4:
        if word_exists(password[0:-2]):  # Check without last two characters
            return False
        if word_exists(password[2:]):  # Check without first two characters
            return False
    if len(password) > 5:
        if word_exists(password[0:-3]):  # Check without last three characters
            return False
        if word_exists(password[3:]):  # Check without first three characters
            return False
    return True

# Check if password has been breached
def check_breached(password):
    # Required: A descriptive user agent must be set describing the application consuming
    #   the HIBP API
    pyhibp.set_user_agent(ua="HildaHackPasswordChecker/0.0.1 (password checker)")

    # Check a password to see if it has been disclosed in a public breach corpus
    resp = pw.is_password_breached(password=password)
    if resp:        
        return False # Password not OK - has been breached
    else:        
        return True # Password OK - not breached
    

# Create List of password tests
password_tests = [
  PasswordTest("Length >= 8",                          check_length_8,   50,  0),
  PasswordTest("Length >= 13",                         check_length_13,  30,  0),
  PasswordTest("Contains upper and lowercase letters", check_case,       10, 26),
  PasswordTest("Contains numbers",                     check_num,        10, 10),
  PasswordTest("Contains symbols",                     check_symbol,     10, 32),
  PasswordTest("Not based on a dictionary word",       check_dictionary, 50,  0),
  PasswordTest("Hasn't been breached",                 check_breached,   30,  0, delayed=True),
]

# Check if password tests are supported
def check_password_tests():
    for test in password_tests:
        try: 
            test.func('password')
        except: # If test is not supported, disable it
            test.text = test.text + ' (not supported)'
            test.disabled = True

# Initialise password tests
def init_password_tests():
    load_word_list()
    check_password_tests()
