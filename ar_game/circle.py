from pyglet import shapes
from random import randint

class Circle:

    min_radius = 10
    max_radius = 30
    colors = [(255, 0, 0), (0, 255, 0)]
    
    def __init__(self, window_width, window_height):
        self.x = randint(Circle.min_radius, window_width)
        self.y = randint(Circle.max_radius, window_height)
        self.radius = randint(Circle.min_radius, Circle.max_radius)
        self.color = Circle.colors[randint(0, 1)]

        self.shape = shapes.Circle(self.x, self.y, self.radius, color=self.color)

    def draw(self):
        self.shape.draw()