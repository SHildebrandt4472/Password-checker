#test changes

import gooeypie as gp
import pyhibp
from pyhibp import pwnedpasswords as pw
from dict import load_word_list, word_exists
import pyperclip
from info_window import InfoWindow

app = gp.GooeyPieApp('Hello!')

app.width = 250
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

def test_password_checks():
    for test in password_tests:
        try:
            test.func('password')
        except:
            test.text = test.text + ' (not supported)'
            test.disabled = True

def open_function():
    app.set_interval(100, timertick)
    check_password(None)  # Initialize icons

def copy(event):
    if password_inp.text == '':
        return
    pyperclip.copy(password_inp.text)
    copy_img.image = 'images/clipboard_tick_hover.png'

def unhover_copy(event):
    if copy_img.image == 'images/clipboard_tick_hover.png':
        copy_img.image = 'images/clipboard_tick.png'
    if copy_img.image == 'images/clipboard_hover.png':
        copy_img.image = 'images/clipboard.png'

def hover_copy(event):
    if copy_img.image == 'images/clipboard_tick.png':
        copy_img.image = 'images/clipboard_tick_hover.png'
    if copy_img.image == 'images/clipboard.png':
        copy_img.image = 'images/clipboard_hover.png'

def reveal(event):
    password_inp.unmask()

def hide(event):
    password_inp.mask()

def show_eye_click(event):
    global password_hidden
    if password_hidden:
        password_hidden = False
        password_inp.unmask()
        show_eye.image = 'images/eye_open_hover.png'
    else:
        password_hidden = True
        password_inp.mask()
        show_eye.image = 'images/eye_closed_hover.png'

def show_eye_hover(event):
    
    if password_hidden:
        show_eye.image = 'images/eye_closed_hover.png'
    else:
        show_eye.image = 'images/eye_open_hover.png'

def show_eye_mouse_out(event):
    if password_hidden:
        show_eye.image = 'images/eye_closed.png'
    else:
        show_eye.image = 'images/eye_open.png'

def more_info(event):
    InfoWindow(app).show_on_top()

def more_info_hover(event):
    info_img.image = 'images/info_hover.png'

def more_info_unhover(event):
    info_img.image = 'images/info.png'

def check_length_8(password):
    if len(password) >= 8:
        return True
    else:
        return False

def check_length_13(password):
    if len(password) >= 13:
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

def brute_force_time(possibilites):
    # 1 billion guesses per second
    seconds = possibilites / 1000000000
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365
    
    if minutes < 1:
        return 'Instantly'
    
    elif hours < 1:
        return f'{minutes:.0f} minutes'
    elif days < 1:
        return f'{hours:.0f} hours'
    elif years < 1:
        return f'{days:.0f} days'
    elif years < 100:
        return f'{years:.0f} years'
    else:
        return 'Not in your lifetime'

def check_password(event):
    pw = password_inp.text
    score = 0
    score_total = 0
    max_chars = 26

    for test in password_tests:
        score_total += test.score

        if test.disabled:
            test.icon.image = 'images/disabled.png'
            continue  # Skip tests if disabled

        if len(pw) == 0:
            test.icon.image = 'images/dash.png'
            continue  # Skip tests if password is empty

        if test.delayed and delay_timer > 0:
            test.icon.image = 'images/dash.png'
            continue  # Skip test if delayed

        ok = test.func(pw)
        if ok:
            test.icon.image = 'images/tick.png'
            score += test.score
            max_chars += test.char_count
        else:
            test.icon.image = 'images/cross.png'
    strength_pb.value = 100/score_total * score
    print(strength_pb.value)

    if len(pw) >0:
        for desc in password_descriptions:
            if strength_pb.value <= desc.score:
                strength_lbl.text = desc.text
                strength_lbl.color = desc.colour
                break
        guesses_lbl.text = brute_force_time(max_chars ** len(pw))
    else:
        strength_lbl.text = ''
        guesses_lbl.text = ''

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
    def __init__(self, text, func, score, char_count, delayed=False):
        self.text = text
        self.func = func
        self.score = score
        self.icon = None
        self.char_count = char_count
        self.delayed = delayed
        self.disabled = False 

class PaswordDescription:
    def __init__(self, text, score, colour):
        self.text = text
        self.score = score
        self.colour = colour

# Create checkboxes
password_tests = [
  PasswordTest("Length >= 8",                          check_length_8,   50,  0),
  PasswordTest("Length >= 13",                         check_length_13,  30,  0),
  PasswordTest("Contains upper and lowercase letters", check_case,       10, 26),
  PasswordTest("Contains numbers",                     check_num,        10, 10),
  PasswordTest("Contains symbols",                     check_symbol,     10, 32),
  PasswordTest("Not based on a dictionary word",       check_dictionary, 50,  0),
  PasswordTest("Hasn't been breached",                 check_breached,   30,  0, delayed=True),
]
test_password_checks()

password_descriptions = [
    PaswordDescription("Very weak",    50, '#ff0000'),
    PaswordDescription("Weak",         70, '#ff4000'),
    PaswordDescription("Fair",         80, '#ff7000'),
    PaswordDescription("Strong",       95, '#008000'),
    PaswordDescription("Very strong", 100, '#08ae00')
]

# Initialize window

app.on_open(open_function)
app.set_grid(6, 1)

row = 1

title_cont = gp.Container(app)
title_cont.set_grid(2, 2)
title_cont.set_column_weights(1, 0)

title_lbl = gp.StyleLabel(title_cont, 'Hilda Hack')
title_lbl.font_size = 15
title_lbl.font_weight = 'bold'
title_cont.add(title_lbl, 1, 1, align='left')

logo = gp.Image(title_cont, 'images/logo.png')
title_cont.add(logo, 1, 2, align='right',row_span=2, valign='middle')

name_lbl = gp.Label(title_cont, 'Enter your password')
title_cont.add(name_lbl, 2, 1, align='left')

app.add(title_cont, row, 1, fill=True)

password_con = gp.Container(app) 
password_con.set_grid(1, 3)
password_inp = gp.Secret(password_con)
password_inp.justify = 'left'
password_inp.width = 30
password_inp.add_event_listener('change', password_changed)
row += 1
password_con.add(password_inp, 1, 1, align='left')

show_eye = gp.Image(password_con, 'images/eye_closed.png')
password_hidden = True
show_eye.add_event_listener('mouse_down', show_eye_click)
show_eye.add_event_listener('mouse_over', show_eye_hover)
show_eye.add_event_listener('mouse_out', show_eye_mouse_out)

password_con.add(show_eye, 1, 2, align='center', valign='middle')

copy_img = gp.Image(password_con, 'images/clipboard.png')
copy_img.add_event_listener('mouse_down', copy)
copy_img.add_event_listener('mouse_out', unhover_copy)
copy_img.add_event_listener('mouse_over', hover_copy)

password_con.add(copy_img, 1, 3, align='center')

app.add(password_con, row, 1, align='left', margins = [0, 15, 0, 15])

# Create checkboxes
checkbox_grid = gp.Container(app) 
checkbox_grid.set_grid(len(password_tests), 2) 
r = 1
for test in password_tests:
    test.icon = gp.Image(checkbox_grid, "images/dash.png")
    label = gp.Label(checkbox_grid, test.text)
    checkbox_grid.add(test.icon, r, 1)
    checkbox_grid.add(label, r, 2)
    r += 1

row += 1
app.add(checkbox_grid, row, 1, align='left')

row += 1
app.add(gp.Separator(app, 'horizontal'), row, 1)

strength_grid = gp.Container(app)
strength_grid.set_grid(2, 2)
lbl = gp.StyleLabel(strength_grid, 'Password Strength:')
lbl.font_weight = 'bold'
strength_lbl = gp.StyleLabel(strength_grid, '')
strength_lbl.font_weight = 'bold'

strength_grid.add(lbl, 1, 1, align='left')
strength_grid.add(strength_lbl, 1, 2, align='left')

lbl = gp.StyleLabel(strength_grid, 'Time to crack:')
lbl.font_weight = 'bold'
guesses_lbl = gp.Label(strength_grid, '')

strength_grid.add(lbl, 2, 1, align='left')
strength_grid.add(guesses_lbl, 2, 2, align='left')


row +=1
app.add(strength_grid, row, 1, align='left')

progress_cont =gp.Container(app)
progress_cont.set_grid(1, 2)
progress_cont.set_column_weights(1, 0)

strength_pb = gp.Progressbar(progress_cont)
#strength_pb.width = 250
progress_cont.add(strength_pb, 1, 1, fill=True)

info_img = gp.Image(progress_cont, 'images/info.png')
info_img.add_event_listener('mouse_down', more_info)
info_img.add_event_listener('mouse_over', more_info_hover)
info_img.add_event_listener('mouse_out', more_info_unhover)
info_img.width = 30
progress_cont.add(info_img, 1, 2,align='center')

row +=1
app.add(progress_cont, row, 1, fill=True)

app.run()