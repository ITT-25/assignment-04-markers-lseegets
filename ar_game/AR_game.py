import cv2
import numpy as np
import pyglet
from PIL import Image
import sys
import math

from circle import Circle
from aruco_sample import display_board

CUTOFF = 130

video_id = 0
# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

# WINDOW_WIDTH = 640
# WINDOW_HEIGHT = 480
WINDOW_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
WINDOW_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
destination = np.float32(np.array([[0, 0], [WINDOW_WIDTH, 0], [WINDOW_WIDTH, WINDOW_HEIGHT], [0, WINDOW_HEIGHT]]))

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

circles = []
circles.append(Circle(WINDOW_WIDTH, WINDOW_HEIGHT))
circles.append(Circle(WINDOW_WIDTH, WINDOW_HEIGHT))
circles.append(Circle(WINDOW_WIDTH, WINDOW_HEIGHT))
circles.append(Circle(WINDOW_WIDTH, WINDOW_HEIGHT))
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

@window.event
def on_draw():
    window.clear()
    ret, frame = cap.read()
    board = display_board(frame, destination, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Display the board if it got detected
    if board is not None:
      img_gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
      ret, thresh = cv2.threshold(img_gray, CUTOFF, 255, cv2.THRESH_BINARY)

      # Find contours (of hands for example)
      contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
                if circle.color == (255, 0, 0):
                   print("RED CIRCLE")
                circles.remove(circle)
                break
         
    else:
      img = cv2glet(frame, 'BGR')
      img.blit(0, 0, 0)

pyglet.app.run()
