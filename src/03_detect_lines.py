import cv2
import numpy as np
from pathlib import Path


# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = PROJECT_DIR / "input" / "drawing.png"
OUTPUT_DIR = PROJECT_DIR / "output"


# Create the output directory if it does not exist
OUTPUT_DIR.mkdir(exist_ok=True)


# Load the image
image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")


# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Detect edges using the Canny edge detector
edges = cv2.Canny(
    gray,
    50,
    150
)


# Detect line segments using the probabilistic Hough transform
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=30,
    maxLineGap=10
)


# Create a copy of the original image for visualization
debug_image = image.copy()


# Draw all detected line segments
if lines is not None:
    for line in lines:

        # Convert the detected line to a flat array
        x1, y1, x2, y2 = line.flatten()

        cv2.line(
            debug_image,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 0, 255),
            2
        )


# Print the number of detected lines
line_count = 0 if lines is None else len(lines)

print(f"Detected lines: {line_count}")

if lines is not None:
    print(f"Lines array shape: {lines.shape}")


# Save the results
cv2.imwrite(
    str(OUTPUT_DIR / "edges.png"),
    edges
)

cv2.imwrite(
    str(OUTPUT_DIR / "detected_lines.png"),
    debug_image
)


# Display the results
cv2.imshow("Original", image)
cv2.imshow("Edges", edges)
cv2.imshow("Detected Lines", debug_image)


# Wait until a key is pressed
cv2.waitKey(0)


# Close all OpenCV windows
cv2.destroyAllWindows()