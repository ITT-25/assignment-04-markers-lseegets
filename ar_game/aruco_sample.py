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

# Camera resolution
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
destination = np.float32(np.array([[0, 0], [width, 0], [width, height], [0, height]]))


# Return a numpy array with values sorted by position to match the destination matrix
def sort_markers(arr):
    arr_np = np.array(arr)

    # Sort points by their y-coordinate
    sort_y = sorted(arr_np, key=lambda x: x[1])

    # Split points into top and bottom
    top_y = sort_y[:2]
    bottom_y = sort_y[2:]

    # Sort points by position
    top_left = min(top_y, key=lambda x: x[0])
    top_right = max(top_y, key=lambda x: x[0])
    bottom_left = min(bottom_y, key=lambda x: x[0])
    bottom_right = max(bottom_y, key=lambda x: x[0])

    return np.float32(np.array([top_left, top_right, bottom_right, bottom_left]))


while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

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
            arr = sort_markers(positions)
            mat = cv2.getPerspectiveTransform(arr, destination)
            frame = cv2.warpPerspective(frame, mat, (width, height))

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press and check if it's the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
