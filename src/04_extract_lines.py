import cv2
import json
import math
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

# Detect edges
edges = cv2.Canny(
    gray,
    50,
    150
)

# Detect line segments
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=30,
    maxLineGap=10
)

# Create a copy for visualization
debug_image = image.copy()

# Store extracted line information
line_data = []

if lines is not None:
    for index, line in enumerate(lines, start=1):

        # Convert the line to a flat array
        x1, y1, x2, y2 = line.flatten()

        # Convert NumPy values to normal Python integers
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # Calculate line length
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx ** 2 + dy ** 2)

        # Calculate line angle in degrees
        angle = math.degrees(math.atan2(dy, dx))

        # Calculate line center
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Create a unique line ID
        line_id = f"L{index:03d}"

        # Store line information
        line_info = {
            "id": line_id,
            "start": {
                "x": x1,
                "y": y1
            },
            "end": {
                "x": x2,
                "y": y2
            },
            "center": {
                "x": round(center_x, 2),
                "y": round(center_y, 2)
            },
            "length_px": round(length, 2),
            "angle_deg": round(angle, 2)
        }

        line_data.append(line_info)

        # Draw the detected line
        cv2.line(
            debug_image,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2
        )

        # Draw the line ID near the center
        cv2.putText(
            debug_image,
            line_id,
            (int(center_x), int(center_y)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 0, 0),
            1,
            cv2.LINE_AA
        )

# Save line data as JSON
json_path = OUTPUT_DIR / "lines.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(
        line_data,
        file,
        indent=4
    )

# Save debug image
debug_path = OUTPUT_DIR / "lines_with_ids.png"

cv2.imwrite(
    str(debug_path),
    debug_image
)

# Print summary
print(f"Detected lines: {len(line_data)}")
print(f"JSON saved to: {json_path}")
print(f"Debug image saved to: {debug_path}")

# Display the result
cv2.imshow("Lines with IDs", debug_image)

cv2.waitKey(0)
cv2.destroyAllWindows()