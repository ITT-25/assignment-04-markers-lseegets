from pyglet import shapes
from random import randint

class Circle:

    min_radius = 10
    max_radius = 30
    colors = [(255, 0, 0), (0, 255, 0)]
    time_to_self_destruction = 5
    
    def __init__(self, window_width, window_height):
        self.x = randint(Circle.max_radius, window_width)
        self.y = randint(Circle.max_radius, window_height)
        self.radius = randint(Circle.min_radius, Circle.max_radius)
        self.color = Circle.colors[randint(0, 1)]

        # Circles get destroyed after [time_to_self_destruction] seconds to avoid the game getting
        # stuck with only red ones
        self.time_to_self_destruction = Circle.time_to_self_destruction

        self.shape = shapes.Circle(self.x, self.y, self.radius, color=self.color)

    def draw(self):
        self.shape.draw()