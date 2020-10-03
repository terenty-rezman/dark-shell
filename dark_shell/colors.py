
def pallete_256():
    template = "\u001b[38;5;{}m"

    NONE = "\u001b[0m"

    PINK = template.format(200)
    RED = template.format(203)
    BLUE = template.format(75)
    GREEN = template.format(85)
    YELLOW = template.format(220)
    DARK = template.format(8)
    GREY = template.format(245)
    BLACK = template.format(238)

    return NONE, PINK, RED, BLUE, GREEN, YELLOW, DARK, GREY, BLACK


def fill_colors():
    return pallete_256()


(
    NONE,
    PINK,
    RED,
    BLUE,
    GREEN,
    YELLOW,
    DARK,
    GREY,
    BLACK
) = fill_colors()
