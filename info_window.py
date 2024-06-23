import gooeypie as gp

class InfoWindow(gp.Window):
    def __init__(self,parent):
        super().__init__(parent, 'Test Window')
        self.width = 300
        self.ok_btn = gp.Button(self, 'OK', self.ok_btn_click)

        self.set_grid(9, 2)
        lbl = gp.StyleLabel(self, 'Hilda Hack')
        lbl.font_weight='bold'
        lbl.font_size=15
        self.add(lbl, 1, 1, align='left')

        lbl = gp.StyleLabel(self, 'Hilda Hack was developed by Samuel Hildebrandt and it has been released using a Mozilla Public License 2.0. \nIt currently supports the following features:')
        self.add(lbl, 2, 1, align='left', column_span=2)

        lbl = gp.StyleLabel(self, 'Password Length')
        lbl.font_weight='bold'
        self.add(lbl, 3, 1, align='left')

        lbl = gp.StyleLabel(self, 'Checks for length of 8, or 12 for better strength')
        self.add(lbl, 3, 2, align='left')

        self.add(self.ok_btn, 9, 1, align='center')

    def ok_btn_click(self, event):
        self.hide()