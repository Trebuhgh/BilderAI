import json
from pathlib import Path


# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = PROJECT_DIR / "output" / "lines.json"


# Define tolerances
ANGLE_TOLERANCE = 5
Y_TOLERANCE = 4
MIN_OVERLAP_RATIO = 0.8


# Load detected lines
with open(JSON_PATH, "r", encoding="utf-8") as file:
    lines = json.load(file)


# Store horizontal lines
horizontal_lines = []


# Find approximately horizontal lines
for line in lines:
    angle = line["angle_deg"]

    # Normalize the angle to a range from 0 to 180 degrees
    normalized_angle = angle % 180

    if (
        normalized_angle <= ANGLE_TOLERANCE
        or normalized_angle >= 180 - ANGLE_TOLERANCE
    ):
        horizontal_lines.append(line)


def get_horizontal_range(line):
    """Return the left and right X coordinate of a horizontal line."""

    x1 = line["start"]["x"]
    x2 = line["end"]["x"]

    return min(x1, x2), max(x1, x2)


def get_average_y(line):
    """Calculate the average Y position of a line."""

    y1 = line["start"]["y"]
    y2 = line["end"]["y"]

    return (y1 + y2) / 2


def get_overlap_ratio(line_a, line_b):
    """Calculate the overlap ratio of two horizontal lines."""

    a_start, a_end = get_horizontal_range(line_a)
    b_start, b_end = get_horizontal_range(line_b)

    # Calculate the overlapping section
    overlap_start = max(a_start, b_start)
    overlap_end = min(a_end, b_end)

    # Calculate the overlap length
    overlap_length = max(0, overlap_end - overlap_start)

    # Calculate the length of both lines
    length_a = a_end - a_start
    length_b = b_end - b_start

    # Use the shorter line as the reference
    shorter_length = min(length_a, length_b)

    # Avoid division by zero
    if shorter_length == 0:
        return 0.0

    # Calculate the overlap ratio
    return overlap_length / shorter_length


# Store possible duplicate pairs
duplicate_pairs = []


# Compare every horizontal line with every following horizontal line
for i in range(len(horizontal_lines)):

    line_a = horizontal_lines[i]

    for j in range(i + 1, len(horizontal_lines)):

        line_b = horizontal_lines[j]

        # Calculate the average Y position of both lines
        y_a = get_average_y(line_a)
        y_b = get_average_y(line_b)

        # Calculate the vertical distance between the lines
        y_distance = abs(y_a - y_b)

        # Calculate how much the two lines overlap
        overlap_ratio = get_overlap_ratio(line_a, line_b)

        # Mark the lines as possible duplicates if they are
        # close enough and overlap strongly enough
        if (
            y_distance <= Y_TOLERANCE
            and overlap_ratio >= MIN_OVERLAP_RATIO
        ):
            duplicate_pairs.append(
                {
                    "line_a": line_a["id"],
                    "line_b": line_b["id"],
                    "y_distance": round(y_distance, 2),
                    "overlap_ratio": round(overlap_ratio, 2),
                }
            )


# Print results
print(f"Horizontal lines: {len(horizontal_lines)}")
print(f"Possible duplicate pairs: {len(duplicate_pairs)}")


for pair in duplicate_pairs:
    print(
        f'{pair["line_a"]} <-> {pair["line_b"]} '
        f'| Y distance: {pair["y_distance"]} px '
        f'| Overlap: {pair["overlap_ratio"] * 100:.0f}%'
    )