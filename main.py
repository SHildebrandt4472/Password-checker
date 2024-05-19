#test changes

import gooeypie as gp

app = gp.GooeyPieApp('Hello!')

app.width = 600
app.height = 400
app.title = "Password Checker"

def copy(event):
    pass

def reveal(event):
    password_inp.toggle()

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
    return False

def check_breached(password):
    return False

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
  PasswordTest("Dosn't contain dictionary words", check_dictionary, 10),
  PasswordTest("Already breached password", check_breached, 10),
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

# Create checkboxes

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