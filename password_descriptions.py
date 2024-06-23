class PaswordDescription:
    def __init__(self, text, score, colour):
        self.text = text
        self.score = score
        self.colour = colour

# Password strength descriptions
password_descriptions = [
    PaswordDescription("Very weak",    50, '#ff0000'),
    PaswordDescription("Weak",         70, '#ff4000'),
    PaswordDescription("Fair",         80, '#ff7000'),
    PaswordDescription("Strong",       95, '#008000'),
    PaswordDescription("Very strong", 100, '#08ae00')
]