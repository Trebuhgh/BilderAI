import json
from pathlib import Path


# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = PROJECT_DIR / "output" / "lines.json"


# Load detected lines
with open(JSON_PATH, "r", encoding="utf-8") as file:
    lines = json.load(file)


# Group lines by their orientation
horizontal_lines = []
vertical_lines = []
diagonal_lines = []


for line in lines:
    angle = line["angle_deg"]

    # Normalize the angle to a range from 0 to 180 degrees
    normalized_angle = angle % 180

    # Detect approximately horizontal lines
    if normalized_angle <= 5 or normalized_angle >= 175:
        horizontal_lines.append(line)

    # Detect approximately vertical lines
    elif 85 <= normalized_angle <= 95:
        vertical_lines.append(line)

    # Everything else is considered diagonal
    else:
        diagonal_lines.append(line)


# Print statistics
print(f"Total lines:      {len(lines)}")
print(f"Horizontal lines: {len(horizontal_lines)}")
print(f"Vertical lines:   {len(vertical_lines)}")
print(f"Diagonal lines:   {len(diagonal_lines)}")