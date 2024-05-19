#test changes

import gooeypie as gp

app = gp.GooeyPieApp('Hello!')

app.width = 600
app.height = 400
app.title = "Password Checker"

def copy(event):
    pass

def reveal(event):
    pass

def more_info(event):
    pass

def check_length(password):
    return False

def check_case(password):
    return True

def check_num(password):
    return True

def check_symbol(password):
    return True

def check_dictionary(password):
    return True

def check_breached(password):
    return True

def check_password(event):
    pw = password_inp.text
    for test in password_tests:
        ok = test.func(pw)
        test.checkbox.checked = ok


class PasswordTest:
    def __init__(self, text, func, score):
        self.text = text
        self.func = func
        self.score = score
        self.checkbox = None    

# Create checkboxes
password_tests = [
  PasswordTest("Length > 12", check_length, 10),
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

password_inp = gp.Input(app)
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
strength_pb.value = 25
row +=1
col =1
app.add(strength_pb, row, col, fill=True)

debug_btn = gp.Button(app, 'Test', check_password)
row +=1
app.add(debug_btn, row, col, align='center')

app.run()

# .secret