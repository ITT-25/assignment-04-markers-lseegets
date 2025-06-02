[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/-leASaOw)

# Setup
- Create and run a virtual environment (on Windows):
    ```
    py -m venv venv
    venv\Scripts\activate
    ```

- Install requirements:

    ```
    pip install -r requirements.txt
    ```

# Perspective Transformation
- Run the program with the following commands:

    ```
    cd perspective_transformation
    py image_extractor.py
    ```

- Specify the input file path, output file path, and desired resolution in the command line.
- A window will open displaying the input image. To extract a rectangular region, click four corner points on the image in order. For best results and minimal distortion, select the points in a consistent direction — either clockwise or counterclockwise.
If you want to preserve the original orientation, start from the top-left corner and proceed clockwise.
- Once four points have been selected, a new window with the extracted region displayed as a rectangle will open.
- If you are dissatisfied with the result, press ESC to start over.
- If you would like to save the result, press the 's' key. The image will be saved to the path specified in the command line earlier.

# AR Game

## Requirements
- A webcam
- A rectangular board with an AruCo marker in each corner

## Playing the Game
- Run the program with the following commands:

    ```
    cd ar_game
    py AR_game.py
    ```

- Position yourself in front of your webcam so that all markers are clearly visible. Once the markers are detected, the board will automatically adjust to match your webcam’s resolution.
- Press SPACE to start the game.
- Use your hands to destroy as many circles as you can in a given time. Green circles will increase your score. Red circles will result in a penalty.
- Once the time has elapsed, your score will be displayed on the screen. Press SPACE to restart the game.

# AR Game - now 3D

## Requirements
-  A webcam
- Two AruCo markers (IDs 4 and 5)

## Playing the Game
- Run the program with the following commands:

    ```
    cd ar_game_3d
    py AR_game_3d.py
    ```

- Position the two markers in front of your webcam so that they are both recognized.
- Make sure they are both visible at the same time and see what happens.

## Sources
Pokéball 3D Model by mitshaker ([Free3D](https://free3d.com/3d-model/pokeball-98387.html))