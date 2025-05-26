import cv2
import numpy as np

input_file = input("Path to input file: ")
#file_destination = input("Output directory: ")
#res = input("Resolution: ")

input_points = []
img_transformed = None

#img = cv2.imread('sample_image.jpg')
img = cv2.imread(input_file)
HEIGHT, WIDTH, _ = img.shape
DESTINATION = np.float32(np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]]))
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

def extract_image(input_points):
    global img_transformed
    arr = np.float32(np.array(input_points))
    mat = cv2.getPerspectiveTransform(arr, DESTINATION)
    img_transformed = cv2.warpPerspective(img, mat, (WIDTH, HEIGHT))
    cv2.imshow("Extracted Rectangle", img_transformed)


cv2.imshow(WINDOW_NAME, img)

cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

cv2.waitKey(0)

while True:
    key = cv2.waitKey(0)
    if key == 27:   # ESCAPE key
        input_points = []
        img = cv2.imread('sample_image.jpg')
        cv2.imshow(WINDOW_NAME, img)
        if cv2.getWindowProperty('Extracted Rectangle', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Extracted Rectangle")
    elif key == ord('s'):
        if cv2.getWindowProperty('Extracted Rectangle', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.imwrite('extracted_output.jpg', img_transformed)