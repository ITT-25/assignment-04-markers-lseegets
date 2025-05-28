from pyglet import text

class GameManager:

    max_duration = 30

    def __init__(self, width, height):
        self.max_circles = 5
        self.score = 0
        self.width = width
        self.height = height
        self.max_duration = GameManager.max_duration
        self.time_elapsed = 0
        self.started = False
        self.finished = False

    def update_score(self, circle):
        if circle.color == (0, 255, 0):
            self.score += 10
        else:
            self.score -= 10

    def reset_game(self):
        self.finished = False
        self.score = 0
        self.time_elapsed = 0

    def draw_score(self):
        score = text.Label(f'Score: {self.score}', font_name='Courier New', font_size=20, x=self.width-100, y=self.height-30, anchor_x='center')
        score.color = (0, 0, 0)
        score.draw()

    def draw_start_screen(self):
        text.Label('AR GAME', font_name='Courier New', font_size=36, x=self.width//2, y=self.height//2 + 80, anchor_x='center', anchor_y='center').draw()
        text.Label('Use your hands to destroy the green circles.', font_name='Courier New', font_size=15, x=self.width//2, y=self.height//2 + 20, anchor_x='center', anchor_y='center').draw()
        text.Label('Steer clear of the red ones', font_name='Courier New', font_size=15, x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center').draw()
        text.Label('Press SPACE to start', font_name='Courier New', font_size=20, x=self.width//2, y=self.height//2 - 60, anchor_x='center', anchor_y='center').draw()

    def draw_finish_screen(self):
        text.Label("Time's Up!", font_name='Courier New', font_size=36, x=self.width//2, y=self.height//2 + 40, anchor_x='center', anchor_y='center').draw()
        text.Label(f'Your Score: {self.score}', font_name='Courier New', font_size=20, x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center').draw()
        text.Label('Press SPACE to restart', font_name='Courier New', font_size=20, x=self.width//2, y=self.height//2 - 40, anchor_x='center', anchor_y='center').draw()