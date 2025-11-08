import cv2 as cv
import numpy as np
from pathlib import Path

from working_with_files import get_all_files_in_dir

GIVEN_PATH = Path("test_data/extract_slide_from_white_background/given")
ALL_SLIDES_PATH = Path("slides")

def calculate_white_ratio(image_path):
    img = cv.imread(str(image_path))
    h, w, _ = img.shape

    # Define the color range for white
    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255])

    # Create a mask for the white color
    mask = cv.inRange(img, lower_white, upper_white)

    # Calculate the ratio of white pixels
    white_pixels = cv.countNonZero(mask)
    total_pixels = h * w
    white_ratio = white_pixels / total_pixels

    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        return white_ratio, 0

    # Find the largest contour
    largest_contour = max(contours, key=cv.contourArea)
    contour_area = cv.contourArea(largest_contour)
    contour_ratio = contour_area / total_pixels

    return white_ratio, contour_ratio

if __name__ == "__main__":
    print("Analyzing white ratio for test images:")
    test_images = get_all_files_in_dir(GIVEN_PATH)
    for image_path in test_images:
        white_ratio, contour_ratio = calculate_white_ratio(image_path)
        print(f"{image_path.name}: White Ratio={white_ratio:.4f}, Contour Ratio={contour_ratio:.4f}")

    print("\nAnalyzing white ratio for all slides:")
    all_slides = get_all_files_in_dir(ALL_SLIDES_PATH)
    for image_path in all_slides:
        white_ratio, contour_ratio = calculate_white_ratio(image_path)
        print(f"{image_path.name}: White Ratio={white_ratio:.4f}, Contour Ratio={contour_ratio:.4f}")
