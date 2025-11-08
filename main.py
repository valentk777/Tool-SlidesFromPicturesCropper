import os
from datetime import datetime
from pathlib import Path

import cv2 as cv

from extractors import extract_slide_from_white_background
from paths import SLIDES_PATH, RESULT_PATH
from working_with_files import get_all_files_in_dir, check_for_duplicates_and_remove_if_exist


def extract_images_using_multiple_iterators(_image_path: Path):
    final_image = extract_slide_from_white_background(_image_path)

    if final_image is not None:
        return final_image

    # we will call another extractor until we will manage to extract image


def show_image(_image):
    cv.imshow("Image", _image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def save_image(_image, name="", output_path: Path = RESULT_PATH):
    if not output_path.exists():
        os.makedirs(output_path)
    cv.imwrite(str(output_path / name), _image)


if __name__ == "__main__":
    iteration_path = RESULT_PATH / f"iteration-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    iteration_path.mkdir(parents=True, exist_ok=True)

    images = get_all_files_in_dir(SLIDES_PATH)

    for image_path in images:
        detected_slide = extract_images_using_multiple_iterators(image_path)
        if detected_slide is not None:
            save_image(detected_slide, image_path.name, iteration_path)

    check_for_duplicates_and_remove_if_exist(str(iteration_path))
