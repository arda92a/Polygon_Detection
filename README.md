# Shape Detection Using OpenCV

This project detects various geometric shapes (triangles, rectangles, pentagons, hexagons) in real-time video using OpenCV. The program captures video from the webcam, processes the frames to identify shapes based on color thresholds set via trackbars, and displays the results.

## Requirements

- Python 3.x
- OpenCV
- NumPy

## Installation

First, make sure you have Python and pip installed. Then, install the required libraries using the following commands:

```bash
pip install opencv-python numpy
````

## Processing the Frame Before Contour Detection

Before detecting contours, the frame undergoes several preprocessing steps to isolate the shapes based on the specified color range. Here's a detailed explanation of these steps:

1. **Capture the Frame**:
    ```python
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    ```
    - `ret, frame = cap.read()`: Captures a frame from the webcam.
    - `frame = cv2.flip(frame, 1)`: Flips the frame horizontally for a mirror effect.

2. **Retrieve Trackbar Positions**:
    ```python
    lower_h = cv2.getTrackbarPos("Lower-Hue", "Settings")
    lower_s = cv2.getTrackbarPos("Lower-Saturation", "Settings")
    lower_v = cv2.getTrackbarPos("Lower-Value", "Settings")
    upper_h = cv2.getTrackbarPos("Upper-Hue", "Settings")
    upper_s = cv2.getTrackbarPos("Upper-Saturation", "Settings")
    upper_v = cv2.getTrackbarPos("Upper-Value", "Settings")
    ```
    - Retrieves the current positions of the trackbars for the lower and upper HSV values.

3. **Define Lower and Upper Color Range**:
    ```python
    lower_color = np.array([lower_h, lower_s, lower_v])
    upper_color = np.array([upper_h, upper_s, upper_v])
    ```
    - `lower_color` and `upper_color` are defined as NumPy arrays using the values obtained from the trackbars.

4. **Convert the Frame to HSV Color Space**:
    ```python
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ```
    - `hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)`: Converts the frame from BGR to HSV color space, which is better for color segmentation.

5. **Create a Mask**:
    ```python
    mask = cv2.inRange(hsv, lower_color, upper_color)
    ```
    - `mask = cv2.inRange(hsv, lower_color, upper_color)`: Creates a binary mask where the pixels within the specified HSV range are white, and all other pixels are black.

6. **Apply Morphological Transformations**:
    ```python
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    ```
    - `kernel = np.ones((5, 5), np.uint8)`: Creates a 5x5 kernel of ones for morphological operations.
    - `mask = cv2.erode(mask, kernel)`: Applies erosion to the mask to remove small white noise. This operation helps to clean up the mask by eroding the boundaries of the white regions.

7. **Find Contours**:
    ```python
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ```
    - `contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)`: Finds contours in the mask. `cv2.RETR_TREE` retrieves all the contours and reconstructs a full hierarchy of nested contours. `cv2.CHAIN_APPROX_SIMPLE` compresses horizontal, vertical, and diagonal segments and leaves only their end points.

By following these preprocessing steps, the script effectively isolates shapes based on their color, making it easier to detect and analyze contours in the subsequent steps.

## Processing the Contours

After finding the contours, each contour is processed to identify the shape. Here are the detailed steps:

1. **Calculate the area of each contour**:
    ```python
    area = cv2.contourArea(cnt)
    ```
    - The `cv2.contourArea(cnt)` function calculates the area of the given contour. This is used to determine the size of the shape.

2. **Approximate the shape of the contour**:
    ```python
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    ```
    - The `cv2.arcLength(cnt, True)` function calculates the perimeter of the contour.
    - `epsilon` is set to 2% of the perimeter and controls the approximation accuracy.
    - The `cv2.approxPolyDP(cnt, epsilon, True)` function approximates the contour to a simpler shape with fewer vertices.

3. **Get the coordinates of the contour**:
    ```python
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    ```
    - `approx.ravel()` flattens the contour coordinates into a single array. `x` and `y` are the first values in this array and are used to position the text.

4. **Identify the shape if the contour area is significant**:
    ```python
    if area > 400:
        cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
    ```
    - `if area > 400:` ensures that only contours with an area greater than 400 are processed.
    - The `cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)` function draws the contour on the frame.

5. **Determine the shape based on the number of vertices and add text to the frame**:
    - **Triangle**:
        ```python
        if len(approx) == 3:
            cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
        ```
        - `len(approx) == 3` checks if the contour has 3 vertices, indicating a triangle.
        - The `cv2.putText` function writes "Triangle" on the frame.

    - **Rectangle**:
        ```python
        elif len(approx) == 4:
            cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
        ```
        - `len(approx) == 4` checks if the contour has 4 vertices, indicating a rectangle.

    - **Pentagon**:
        ```python
        elif len(approx) == 5:
            cv2.putText(frame, "Pentagon", (x, y), font, 1, (0, 0, 0))
        ```
        - `len(approx) == 5` checks if the contour has 5 vertices, indicating a pentagon.

    - **Hexagon**:
        ```python
        elif len(approx) == 6:
            cv2.putText(frame, "Hexagon", (x, y), font, 1, (0, 0, 0))
        ```
        - `len(approx) == 6` checks if the contour has 6 vertices, indicating a hexagon.

    - **Circle**:
        ```python
        elif len(approx) > 6:
            cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
        ```
        - `len(approx) > 6` checks if the contour has more than 6 vertices, indicating a circle.

## Contributing

If you have ideas for improvements or want to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome and appreciated!

## License

This project is licensed under the MIT License.
