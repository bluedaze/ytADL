stripformatting = "\u001b[0m"
clearline = "\r\u001b[2K"
up = "\033[1A"


def bold(text):
    bold_text = "\u001b[1m"
    return r"".join([bold_text, text, stripformatting])


def underline(text):
    stripformatting = "\u001b[0m"
    underline_text = "\u001b[4m"
    return r"".join([underline_text, text, stripformatting])


def color(text, text_color=None):
    color_choices = {
        "black": "\u001b[30m",
        "red": "\u001b[31m",
        "green": "\u001b[32m",
        "yellow": "\u001b[33m",
        "blue": "\u001b[34m",
        "magenta": "\u001b[35m",
        "cyan": "\u001b[36m",
        "white": "\u001b[37m",
        "matrix": "\u001b[38;5;46m",
    }
    if text_color == None:
        choice = color_choices["matrix"]
    else:
        choice = color_choices[text_color]
    return "".join([choice, text, stripformatting])


# returnhome = "\u001b[1000D"

# save = "\u001b[1s"
# goback = "\u001b[1u"

# move = {"up": "\033[1A",
# "down": "\033[1B",
# "right": "\u001b[1C",
# "left": "\u001b[1D",
# "home": "\u001b[1000D"}

# def preferences():
#     downloaded_path = ""
#     plex_preference = ""
#     plex_username = ""
#     plex_password = ""
#     plex_server = ""
#     youtube_dl_preferences = ""
#     silent_mode = ""
#     apikey = ""
