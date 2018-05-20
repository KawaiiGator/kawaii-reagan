import turtle
from PIL import Image


def load_reagan(file_path):
    image = Image.open(file_path)
    turtle.setup(width=image.width,
                 height=image.height)
    turtle_screen = turtle.Screen()
    turtle_screen.bgpic(file_path)
    return turtle_screen
