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

### Display the Frames

1. **Display the original frame with detected shapes**:
    ```python
    cv2.imshow("Frame", frame)
    ```
    - The `cv2.imshow("Frame", frame)` function shows the original video frame with detected shapes and labels.

2. **Display the mask frame**:
    ```python
    cv2.imshow("Mask", mask)
    ```
    - The `cv2.imshow("Mask", mask)` function shows the binary mask frame.

### Exit

1. **Break the loop when 'q' is pressed**:
    ```python
    if cv2.waitKey(3) & 0xFF == ord("q"):
        break
    ```
    - The loop breaks and exits the program when the 'q' key is pressed.

### Cleanup

1. **Release the video capture object and destroy all windows**:
    ```python
    cap.release()
    cv2.destroyAllWindows()
    ```
    - The `cap.release()` function releases the webcam.
    - The `cv2.destroyAllWindows()` function closes all OpenCV windows.
