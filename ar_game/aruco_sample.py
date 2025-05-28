import cv2
import cv2.aruco as aruco
import sys
import numpy as np

video_id = 0
positions = []

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# Define the ArUco dictionary, parameters, and detector
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
aruco_params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, aruco_params)

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

# Return a numpy array with values sorted by position to match the destination matrix
def sort_markers(arr):
    arr_np = np.array(arr)

    # Sort points by their y-coordinate
    sort_y = sorted(arr_np, key=lambda x: x[1])

    # Split sorted points into top and bottom
    top_y = sort_y[:2]
    bottom_y = sort_y[2:]

    # Sort points by position
    top_left = min(top_y, key=lambda x: x[0])
    top_right = max(top_y, key=lambda x: x[0])
    bottom_left = min(bottom_y, key=lambda x: x[0])
    bottom_right = max(bottom_y, key=lambda x: x[0])

    return np.float32(np.array([top_left, top_right, bottom_right, bottom_left]))


def display_board(frame, destination, width, height):
    global detector, positions

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, _ = detector.detectMarkers(gray)

    # Check if marker is detected
    if ids is not None:
        if len(ids) == 4:
            # Draw lines along the sides of the marker
            aruco.drawDetectedMarkers(frame, corners)
            positions.clear()
            for i in range(4):
                marker_corners = corners[i][0]
                pos = np.mean(marker_corners, axis=0)   # Get the center of each marker
                positions.append((pos))
            
            # Sort the markers by their position and transform the board
            arr = sort_markers(positions)
            mat = cv2.getPerspectiveTransform(arr, destination)
            frame = cv2.warpPerspective(frame, mat, (width, height))

            return frame
    
    return None

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
