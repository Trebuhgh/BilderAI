import cv2
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

# Create a binary image using Otsu's automatic threshold
_, binary = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

# Detect edges
edges = cv2.Canny(
    gray,
    50,
    150
)

# Save intermediate results
cv2.imwrite(str(OUTPUT_DIR / "gray.png"), gray)
cv2.imwrite(str(OUTPUT_DIR / "binary.png"), binary)
cv2.imwrite(str(OUTPUT_DIR / "edges.png"), edges)

# Display the results
cv2.imshow("Original", image)
cv2.imshow("Grayscale", gray)
cv2.imshow("Binary", binary)
cv2.imshow("Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()