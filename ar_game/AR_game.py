import cv2
import numpy as np
import pyglet
from pyglet.window import key
from PIL import Image
import sys
import math

from circle import Circle
from game_manager import GameManager
from aruco_sample import display_board

CUTOFF = 130

video_id = 0
# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

# Webcam resolution
WINDOW_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
WINDOW_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
destination = np.float32(np.array([[0, 0], [WINDOW_WIDTH, 0], [WINDOW_WIDTH, WINDOW_HEIGHT], [0, WINDOW_HEIGHT]]))

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
game = GameManager(WINDOW_WIDTH, WINDOW_HEIGHT)

circles = []
for _ in range(game.max_circles):
    circles.append(Circle(WINDOW_WIDTH, WINDOW_HEIGHT))

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img,fmt):
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if fmt == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   fmt=fmt, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg

# Check if
# 1) time limit has been reached
# 2) circles need to be refreshed
def update(dt):
   if game.started and not game.finished:
      if game.time_elapsed <= game.max_duration:
        game.time_elapsed += dt
        for circle in circles:
          circle.time_to_self_destruction -= dt
          if circle.time_to_self_destruction <= 0:
            if circle in circles:
              circles.remove(circle)
      else:
        game.finished = True

pyglet.clock.schedule_interval(update, 0.1)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
      if not game.started:
        game.started = True
      elif game.finished:
        game.reset_game()

@window.event
def on_draw():
    window.clear()

    if not game.started and not game.finished:
       game.draw_start_screen()
    
    elif game.started and not game.finished:
    
      # Fill up on circles if necessary
      if len(circles) < game.max_circles:
        for _ in range(len(circles), game.max_circles):
            circles.append(Circle(WINDOW_WIDTH, WINDOW_HEIGHT))

      _, frame = cap.read()
      board = display_board(frame, destination, WINDOW_WIDTH, WINDOW_HEIGHT)

      # Display the board if it got detected
      if board is not None:
        img_gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, CUTOFF, 255, cv2.THRESH_BINARY)

        # Find contours (of hands for example)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        img = cv2glet(thresh_bgr, 'BGR')
        img.blit(0, 0, 0)

        # For every circle, check if it collides with a point of a contour
        for circle in circles:
          circle.draw()
          for contour in contours:
            for point in contour:
                x, y = point[0]
                y = WINDOW_HEIGHT - y # Flip the y coordinate for pyglet

                # Calculate the Euclidean distance between the contour point and the circle.
                # If dist is smaller than the circle's radius (i.e., the contour point is inside
                # the circle), destroy the circle
                dist = math.dist((x, y), (circle.x, circle.y))
                if dist < circle.radius:
                  if circle in circles:
                    game.update_score(circle)
                    circles.remove(circle)
                  break

        game.draw_score()
          
      else:
        img = cv2glet(frame, 'BGR')
        img.blit(0, 0, 0)

    elif game.started and game.finished:
       game.draw_finish_screen()

pyglet.app.run()
