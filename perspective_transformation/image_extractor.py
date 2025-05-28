import cv2
import numpy as np
import os

# Inputs
input_file = input("Path to the input file: ")
file_destination = input("Full path for the output file (including .jpg extension): ")
res = input("Output resolution in format WIDTHxHEIGHT (e.g., 1920x1080): ")
dest_width, dest_height = map(int, res.lower().split('x'))

input_points = []
img_transformed = None

img = cv2.imread(input_file)
DESTINATION = np.float32(np.array([[0, 0], [dest_width, 0], [dest_width, dest_height], [0, dest_height]]))
WINDOW_NAME = 'Preview Window'

cv2.namedWindow(WINDOW_NAME)

def mouse_callback(event, x, y, flags, param):
    global img, input_points

    if event == cv2.EVENT_LBUTTONDOWN and len(input_points) < 4:
        input_points.append([x, y])
        img = cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(WINDOW_NAME, img)

        if len(input_points) == 4:
            extract_image(input_points)

# Extracting the area between the drawn points
def extract_image(input_points):
    global img_transformed
    arr = np.float32(np.array(input_points))
    mat = cv2.getPerspectiveTransform(arr, DESTINATION)
    img_transformed = cv2.warpPerspective(img, mat, (dest_width, dest_height))
    cv2.imshow("Extracted Image", img_transformed)


cv2.imshow(WINDOW_NAME, img)

cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

while True:
    key = cv2.waitKey(0)

    # Start over by pressing the ESCAPE key
    if key == 27:
        input_points = []
        img = cv2.imread(input_file)
        cv2.imshow(WINDOW_NAME, img)
        if cv2.getWindowProperty('Extracted Image', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Extracted Image")

    # Save the image by pressing 's'
    elif key == ord('s'):
        if cv2.getWindowProperty('Extracted Image', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.imwrite(file_destination, img_transformed)

    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break