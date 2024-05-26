#test changes

import gooeypie as gp
import pyhibp
from pyhibp import pwnedpasswords as pw
from dict import load_word_list, word_exists

app = gp.GooeyPieApp('Hello!')

app.width = 600
app.height = 400
app.title = "Password Checker"

load_word_list()

def copy(event):
    pass

def reveal(event):
    password_inp.unmask()

def hide(event):
    password_inp.mask()

def more_info(event):
    pass

def check_length_8(password):
    if len(password) >= 8:
        return True
    else:
        return False

def check_length_12(password):
    if len(password) >= 12:
        return True
    else:
        return False

def check_case(password):
    upper_count = 0
    lower_count = 0
    for letter in password:
        if letter >= 'A' and letter <= 'Z':
            upper_count += 1
        elif letter >= 'a' and letter <= 'z':
            lower_count += 1

    if upper_count >= 1 and lower_count >= 1:
        return True
    else:
        return False

def check_num(password):
    for letter in password:
        if letter >= '0' and letter <= '9':
            return True
    return False

def check_symbol(password):
    symbols = "`~!@#$%^&*()_+-=[]{}|;:,.<>?/\\\'\""
    for letter in password:
        if letter in symbols:
            return True
    return False

def check_dictionary(password):
    if word_exists(password):
        return False
    return True

def check_breached(password):
    # Required: A descriptive user agent must be set describing the application consuming
    #   the HIBP API
    pyhibp.set_user_agent(ua="BasicPasswordChecker/0.0.1 (password checker)")

    # Check a password to see if it has been disclosed in a public breach corpus
    resp = pw.is_password_breached(password=password)
    if resp:
        print("Password breached!")
        print("This password was used {0} time(s) before.".format(resp))
        return False
    else:
        print("Password not breached!")
        return True

def check_password(event):
    pw = password_inp.text
    score = 0
    score_total = 0
    for test in password_tests:
        ok = test.func(pw)
        test.checkbox.checked = ok
        if ok:
            score += test.score
        score_total += test.score
    strength_pb.value = 100/score_total * score


class PasswordTest:
    def __init__(self, text, func, score):
        self.text = text
        self.func = func
        self.score = score
        self.checkbox = None    

# Create checkboxes
password_tests = [
  PasswordTest("Length >= 8", check_length_8, 5),
  PasswordTest("Length >= 12", check_length_12, 10),
  PasswordTest("Contains upper and lowercase letters", check_case, 10),
  PasswordTest("Contains numbers", check_num, 10),
  PasswordTest("Contains symbols", check_symbol, 10),
  PasswordTest("Not based on a dictionary word", check_dictionary, 10),
  PasswordTest("Hasn't been breached", check_breached, 10),
]


# Initialize window

app.set_grid(6+len(password_tests), 2)

row = 1
col = 1

name_lbl = gp.Label(app, 'Enter your password')
app.add(name_lbl, row, col, align='left')

password_inp = gp.Secret(app)
password_inp.justify = 'left'
password_inp.width = 30
row +=1
app.add(password_inp, row, col, align='left')

copy_btn = gp.Button(app, 'Copy', copy)
col +=1
app.add(copy_btn, row, col, align='center')

show_btn = gp.Button(app, 'Show password', reveal)
col =1
row +=1
app.add(show_btn, row, col, align='left')

show_img = gp.Image(app, 'images/eye.png')
show_img.add_event_listener('mouse_down', reveal)
show_img.add_event_listener('mouse_up', hide)
col +=1
app.add(show_img, row, col, align='center')

# Create checkboxes
col = 1
for test in password_tests:
    test.checkbox = gp.Checkbox(app, test.text)
    row += 1
    app.add(test.checkbox, row, col, align='left')

strength_lbl = gp.Label(app, '')
row +=1
app.add(strength_lbl, row, col, align='left')

more_info_btn = gp.Button(app, 'More info', more_info)
col +=1
app.add(more_info_btn, row, col, align='center')

strength_pb = gp.Progressbar(app)
row +=1
col =1
app.add(strength_pb, row, col, fill=True)

debug_btn = gp.Button(app, 'Test', check_password)
row +=1
app.add(debug_btn, row, col, align='center')

app.run()

# .secret