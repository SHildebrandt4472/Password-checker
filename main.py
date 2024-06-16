#test changes

import gooeypie as gp
import pyhibp
from pyhibp import pwnedpasswords as pw
from dict import load_word_list, word_exists
import pyperclip

app = gp.GooeyPieApp('Hello!')

app.width = 600
app.height = 400
app.title = "Hilda Hack"

load_word_list()
delay_timer = 0

def timertick():
    global delay_timer
    if delay_timer > 0:
        delay_timer -= 1
        if delay_timer == 0:
            check_password(None)

def open_function():
    app.set_interval(100, timertick)

def copy(event):
    if password_inp.text == '':
        return
    pyperclip.copy(password_inp.text)
    copy_img.image = 'images/clipboard_tick.png'

def reveal(event):
    password_inp.unmask()

def hide(event):
    password_inp.mask()

def show_img_click(event):
    global password_hidden
    if password_hidden:
        password_hidden = False
        password_inp.unmask()
        show_img.image = 'images/eye_open_hover.png'
    else:
        password_hidden = True
        password_inp.mask()
        show_img.image = 'images/eye_closed_hover.png'

def show_img_hover(event):
    if password_hidden:
        show_img.image = 'images/eye_closed_hover.png'
    else:
        show_img.image = 'images/eye_open_hover.png'

def show_img_mouse_out(event):
    if password_hidden:
        show_img.image = 'images/eye_closed.png'
    else:
        show_img.image = 'images/eye_open.png'

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
        score_total += test.score
        if len(pw) == 0:
            test.icon.image = 'images/dash.png'
            continue  # Skip tests if password is empty

        if test.delayed and delay_timer > 0:
            test.icon.image = 'images/dash.png'
            continue  # Skip tests if password is empty

        ok = test.func(pw)
        if ok:
            test.icon.image = 'images/tick.png'
            score += test.score
        else:
            test.icon.image = 'images/cross.png'
    strength_pb.value = 100/score_total * score

def password_changed(event):
    global delay_timer
    delay_timer = 8 # Delay for 1 second before checking password
    copy_img.image = 'images/clipboard.png'
    check_password(event)

def debug_1():
    copy(None)

def debug(event):
    app.set_timeout(2000, debug_1)

class PasswordTest:
    def __init__(self, text, func, score, delayed=False):
        self.text = text
        self.func = func
        self.score = score
        self.icon = None
        self.delayed = delayed 

# Create checkboxes
password_tests = [
  PasswordTest("Length >= 8", check_length_8, 5),
  PasswordTest("Length >= 12", check_length_12, 10),
  PasswordTest("Contains upper and lowercase letters", check_case, 10),
  PasswordTest("Contains numbers", check_num, 10),
  PasswordTest("Contains symbols", check_symbol, 10),
  PasswordTest("Not based on a dictionary word", check_dictionary, 10),
  PasswordTest("Hasn't been breached", check_breached, 10, delayed=True),
]


# Initialize window

app.on_open(open_function)
app.set_grid(6+len(password_tests), 2)

row = 1
col = 1

name_lbl = gp.Label(app, 'Enter your password')
app.add(name_lbl, row, col, align='left')

password_con = gp.Container(app) 
password_con.set_grid(1, 3)  
password_inp = gp.Secret(password_con)
password_inp.justify = 'left'
password_inp.width = 30
password_inp.add_event_listener('change', password_changed)
col =1
row += 1
password_con.add(password_inp, 1, 1, align='left')

show_img = gp.Image(password_con, 'images/eye_closed.png')
password_hidden = True
show_img.add_event_listener('mouse_down', show_img_click)
show_img.add_event_listener('mouse_over', show_img_hover)
show_img.add_event_listener('mouse_out', show_img_mouse_out)

password_con.add(show_img, 1, 2, align='center', valign='middle')

copy_img = gp.Image(password_con, 'images/clipboard.png')
copy_img.add_event_listener('mouse_down', copy)

password_con.add(copy_img, 1, 3, align='center')

app.add(password_con, row, col, align='left')

copy_btn = gp.Button(app, 'Copy', copy)
col +=1
app.add(copy_btn, row, col, align='center')

# Create checkboxes
checkbox_grid = gp.Container(app) 
checkbox_grid.set_grid(len(password_tests), 2) 
col = 1
r = 1
for test in password_tests:
    test.icon = gp.Image(checkbox_grid, "images/dash.png")
    label = gp.Label(checkbox_grid, test.text)
    checkbox_grid.add(test.icon, r, 1)
    checkbox_grid.add(label, r, 2)
    r += 1

row += 1
app.add(checkbox_grid, row, col, align='left')

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

debug_btn = gp.Button(app, 'Test', debug)
row +=1
app.add(debug_btn, row, col, align='center')

app.run()
