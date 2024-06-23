import gooeypie as gp

class InfoWindow(gp.Window):
    def __init__(self,parent):
        super().__init__(parent, 'Test Window')
        self.width = 300
        self.ok_btn = gp.Button(self, 'Close', self.close_btn_click)

        self.set_grid(9, 2)
        lbl = gp.StyleLabel(self, 'Hilda Hack')
        lbl.font_weight='bold'
        lbl.font_size=15
        self.add(lbl, 1, 1, align='left')

        lbl = gp.StyleLabel(self, 'Hilda Hack was developed by Samuel Hildebrandt and it has been released using a Mozilla Public License 2.0. \nIt currently supports the following features:')
        self.add(lbl, 2, 1, align='left', column_span=2)

        info_text = [['Password Length:', 'Checks for length of 8, or 12 for better strength'],
                     ['Password Complexity:', 'Use letters (upper and lowercase), numbers, and symbols'],
                     ['Dictionary words:', 'Checks against English dictionary of words'],
                     ['Breached Password:', "Checks against the 'Have I been pwned' list of breached passwords"],
                     ['Save to Clipboard:', "Copy your password here. It auto-clears in 2 minutes"]]
        
        row = 3
        for info in info_text:
            lbl = gp.StyleLabel(self, info[0])
            lbl.font_weight='bold'
            self.add(lbl, row, 1, align='left')

            lbl = gp.StyleLabel(self, info[1])
            self.add(lbl, row, 2, align='left')
            row += 1

        self.add(self.ok_btn, 9, 2, align='right')

    def close_btn_click(self, event):
        self.hide()