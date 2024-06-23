import gooeypie as gp
import pyperclip
from info_window import InfoWindow
from password_tests import password_tests, init_password_tests
from password_descriptions import password_descriptions

# Global timer variable to delay checking password after user input
delay_timer = 0

def timertick():
    global delay_timer
    if delay_timer > 0:
        delay_timer -= 1
        if delay_timer == 0:
            check_password(None)

def on_app_open():
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

def brute_force_time(possibilites):
    # Assume 1 billion guesses per second
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


#
#  MAIN: App starts Here
#
if __name__ == '__main__':      

    init_password_tests()  # Initialise all tests

    app = gp.GooeyPieApp('Hilda Hack')    
    app.width = 250
    app.height = 400    
    app.on_open(on_app_open)
    app.set_icon('images/fav_logo.png')

    # Setup main window with widgets
    app.set_grid(6, 1) # Main grid for layout is single column rows

    #
    # Main Grid Row: Title, Logo, Password input label
    #
    row = 1    
    title_cont = gp.Container(app)
    title_cont.set_grid(2, 2)   
    title_cont.set_column_weights(1, 0)

    # Title
    title_lbl = gp.StyleLabel(title_cont, 'Hilda Hack')
    title_lbl.font_size = 15
    title_lbl.font_weight = 'bold'
    title_cont.add(title_lbl, 1, 1, align='left')

    # Logo
    logo = gp.Image(title_cont, 'images/logo.png')
    title_cont.add(logo, 1, 2, align='right',row_span=2, valign='middle')

    # Password input label
    name_lbl = gp.Label(title_cont, 'Enter your password')
    title_cont.add(name_lbl, 2, 1, align='left')

    app.add(title_cont, row, 1, fill=True) # Add title container to app 

    #
    # Main Grid Row: Password input, Show/Hide, Copy
    #
    row += 1
    password_con = gp.Container(app) 
    password_con.set_grid(1, 3)

    # Password input
    password_inp = gp.Secret(password_con)
    password_inp.justify = 'left'
    password_inp.width = 30
    password_inp.add_event_listener('change', password_changed)    
    password_con.add(password_inp, 1, 1, align='left')

    # Show/Hide image button
    show_eye = gp.Image(password_con, 'images/eye_closed.png')
    password_hidden = True
    show_eye.add_event_listener('mouse_down', show_eye_click)
    show_eye.add_event_listener('mouse_over', show_eye_hover)
    show_eye.add_event_listener('mouse_out', show_eye_mouse_out)
    password_con.add(show_eye, 1, 2, align='center', valign='middle')

    # Copy image button
    copy_img = gp.Image(password_con, 'images/clipboard.png')
    copy_img.add_event_listener('mouse_down', copy)
    copy_img.add_event_listener('mouse_out', unhover_copy)
    copy_img.add_event_listener('mouse_over', hover_copy)
    password_con.add(copy_img, 1, 3, align='center')

    app.add(password_con, row, 1, align='left', margins = [0, 15, 0, 15]) # Add password container to app

    #
    # Main Grid Row: Password tests grid
    #
    row += 1
    checkbox_grid = gp.Container(app) 
    checkbox_grid.set_grid(len(password_tests), 2) 

    # Add password tests to grid
    r = 1
    for test in password_tests:
        test.icon = gp.Image(checkbox_grid, "images/dash.png")
        label = gp.Label(checkbox_grid, test.text)
        checkbox_grid.add(test.icon, r, 1)
        checkbox_grid.add(label, r, 2)
        r += 1
    
    app.add(checkbox_grid, row, 1, align='left')

    #
    # Main Grid Row: Separator
    #
    row += 1
    app.add(gp.Separator(app, 'horizontal'), row, 1)

    #
    # Main Grid Row: Password strength grid
    #
    row +=1
    strength_grid = gp.Container(app)
    strength_grid.set_grid(2, 2)

    # Password strength label
    lbl = gp.StyleLabel(strength_grid, 'Password Strength:')
    lbl.font_weight = 'bold'
    strength_grid.add(lbl, 1, 1, align='left')

    # Password strength value
    strength_lbl = gp.StyleLabel(strength_grid, '')
    strength_lbl.font_weight = 'bold'    
    strength_grid.add(strength_lbl, 1, 2, align='left')

    # Time to crack label    
    lbl = gp.StyleLabel(strength_grid, 'Time to crack:')
    lbl.font_weight = 'bold'
    strength_grid.add(lbl, 2, 1, align='left')

    # Time to crack value
    guesses_lbl = gp.Label(strength_grid, '')    
    strength_grid.add(guesses_lbl, 2, 2, align='left')

    app.add(strength_grid, row, 1, align='left')  # Add grid to app

    #
    # Main Grid Row: Progress bar
    #
    row += 1
    progress_cont =gp.Container(app)
    progress_cont.set_grid(1, 2)
    progress_cont.set_column_weights(1, 0)

    # Progress bar
    strength_pb = gp.Progressbar(progress_cont)    
    progress_cont.add(strength_pb, 1, 1, fill=True)

    # Info button
    info_img = gp.Image(progress_cont, 'images/info.png')
    info_img.add_event_listener('mouse_down', more_info)
    info_img.add_event_listener('mouse_over', more_info_hover)
    info_img.add_event_listener('mouse_out', more_info_unhover)
    info_img.width = 30
    progress_cont.add(info_img, 1, 2,align='center')
    
    app.add(progress_cont, row, 1, fill=True) # Add progress container to app


    # Open the main window and run the app
    app.run() 