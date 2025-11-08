import cv2 as cv
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent))

from main import extract_images_using_multiple_iterators
from working_with_files import get_all_files_in_dir

GIVEN_PATH = Path("test_data/extract_slide_from_white_background/given")
ALL_SLIDES_PATH = Path("slides")

def analyze_ratios(image_path):
    original_image = cv.imread(str(image_path))
    original_h, original_w, _ = original_image.shape

    cropped_image = extract_images_using_multiple_iterators(image_path)

    if cropped_image is not None:
        cropped_h, cropped_w, _ = cropped_image.shape
        width_ratio = cropped_w / original_w
        height_ratio = cropped_h / original_h
        return width_ratio, height_ratio
    else:
        return None, None

if __name__ == "__main__":
    print("Analyzing dimension ratios for test images:")
    test_images = get_all_files_in_dir(GIVEN_PATH)
    for image_path in test_images:
        width_ratio, height_ratio = analyze_ratios(image_path)
        if width_ratio is not None:
            print(f"{image_path.name}: Width Ratio={width_ratio:.4f}, Height Ratio={height_ratio:.4f}")

    print("\nAnalyzing dimension ratios for all slides:")
    all_slides = get_all_files_in_dir(ALL_SLIDES_PATH)
    for image_path in all_slides:
        width_ratio, height_ratio = analyze_ratios(image_path)
        if width_ratio is not None:
            print(f"{image_path.name}: Width Ratio={width_ratio:.4f}, Height Ratio={height_ratio:.4f}")
