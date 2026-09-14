import cv2
from pathlib import Path

# Define the project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Define the input image path
IMAGE_PATH = PROJECT_DIR / "input" / "drawing.png"

# Load the image
image = cv2.imread(str(IMAGE_PATH))

# Check whether the image was loaded successfully
if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

# Get image dimensions
height, width = image.shape[:2]

print(f"Image loaded: {IMAGE_PATH}")
print(f"Width:  {width} pixels")
print(f"Height: {height} pixels")

# Display the original image
cv2.imshow("Original", image)

# Wait for a key press before closing the window
cv2.waitKey(0)
cv2.destroyAllWindows()