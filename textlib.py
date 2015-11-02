
class Paragraph:

    def __init__(self, blocks):
        self.blocks = blocks

    def __str__(self):
        text = "Paragraph:\n"
        for i, x in enumerate(self.blocks):
            text += "\t{}: {}\n".format(i, x)
        return text

    __repr__ = __str__


class Text:

    def __init__(self, string):
        self.text = string

    def __str__(self):
        return "Text: '" + self.text + "'"

    __repr__ = __str__
