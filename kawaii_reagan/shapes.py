import math
import turtle
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, center=(0, 0), width=100, height=100, rotation=0):
        self.center = center
        self.width = width
        self.height = height
        self.rotation = rotation
        self.turtle = turtle.Turtle()
        self.turtle.ht()

    @abstractmethod
    def draw(self):
        pass

    def reset(self):
        self.turtle.reset()


class Blush(Shape):
    def __init__(self, color='hotpink', n=4, style='slash', weight=3, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.n = n
        self.style = style
        self.weight = weight

    def _draw_wave(self):
        t = self.turtle
        t.penup()
        start_point = (self.center[0] - (self.width / 2), self.center[1])
        if self.rotation:
            t.goto(rotate_point(start_point,
                                self.rotation,
                                self.center))
        else:
            t.goto(start_point)
        x_offset = self.center[0] - (self.width / 2)
        y_offset = self.center[1]
        t.down()
        for angle in range(360 * self.n):
            x = angle * (self.width / self.n / 360) + x_offset
            y = math.sin(math.radians(angle)) * (self.height / 2) + y_offset
            if self.rotation:
                x, y = rotate_point((x, y), self.rotation, self.center)
            t.goto(x, y)

    def _draw_slash(self):
        t = self.turtle
        x_offset = self.center[0] - (self.width / 2)
        y_offset = self.center[1]
        column_width = self.width / self.n
        for i in range(self.n):
            point1 = (x_offset + (i * column_width) + (1 / 6 * column_width),
                      y_offset - (1 / 2 * self.height))
            point2 = (x_offset + (i * column_width) + (5 / 6 * column_width),
                      y_offset + (1 / 2 * self.height))
            if self.rotation:
                point1 = rotate_point(point1, self.rotation, self.center)
                point2 = rotate_point(point2, self.rotation, self.center)
            t.penup()
            t.goto(point1)
            t.pendown()
            t.goto(point2)

    def draw(self):
        self.turtle.color(self.color)
        self.turtle.pensize(self.weight)

        if self.style == 'wave':
            self._draw_wave()
        elif self.style == 'slash':
            self._draw_slash()
        else:
            raise ValueError


class Bow(Shape):
    def __init__(self, color='lightskyblue', **kwargs):
        super().__init__(**kwargs)
        self.color = color

    def draw(self):
        bow_points = [(0.25, 0.25),
                      (1.0, 0.5),
                      (1.0, -0.5),
                      (0.25, -0.25),
                      (-0.25, -0.25),
                      (-1.0, -0.5),
                      (-1.0, 0.5),
                      (-0.25, 0.25),
                      (0.25, 0.25)]
        scaled_bow = [((point[0] * self.width) + self.center[0],
                       (point[1] * self.height) + self.center[1])
                      for point in bow_points]
        if self.rotation:
            scaled_bow = [rotate_point(point, self.rotation, self.center)
                          for point in scaled_bow]
        t = self.turtle
        t.color(self.color)
        t.fillcolor(self.color)
        t.pensize(0)
        t.penup()
        t.goto(scaled_bow[0])
        t.pendown()
        t.begin_fill()
        for point in scaled_bow:
            t.goto(point)
        t.end_fill()


class Eye(Shape):
    def __init__(self, color='black', catchlight=True, **kwargs):
        super().__init__(**kwargs)
        self.catchlight = catchlight
        self.color = color

    def draw(self):
        def draw_circle(turtle, point, radius):
            turtle.penup()
            turtle.goto(point[0], point[1] - radius)
            turtle.begin_fill()
            turtle.circle(radius=radius)
            turtle.end_fill()

        t = self.turtle
        t.color(self.color)
        t.fillcolor(self.color)
        draw_circle(t, self.center, self.width / 2)
        if self.catchlight:
            catchlight_point_large = rotate_point((self.center[0] + (self.width * 0.3),
                                                   self.center[1]),
                                                  45 + self.rotation,
                                                  self.center)
            catchlight_point_small = rotate_point((self.center[0] + (self.width * .1),
                                                   self.center[1]),
                                                  45 + self.rotation,
                                                  self.center)
            t.fillcolor('white')
            draw_circle(t, catchlight_point_large, self.width / 8)
            draw_circle(t, catchlight_point_small, self.width / 24)


def rotate_point(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    # Source:
    # https://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects/20024348#20024348
    angle_rad = math.radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    tmp_point = (point[0] - center_point[0], point[1] - center_point[1])
    tmp_rotated_point = (tmp_point[0] * math.cos(angle_rad) - tmp_point[1] * math.sin(angle_rad),
                         tmp_point[0] * math.sin(angle_rad) + tmp_point[1] * math.cos(angle_rad))
    # Reverse the shifting we have done
    rotated_point = (tmp_rotated_point[0] + center_point[0], tmp_rotated_point[1] + center_point[1])
    return rotated_point
