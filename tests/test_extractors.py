import sys
from pathlib import Path

# sys.path.append(str(Path(__file__).parent.parent))

import cv2 as cv
import pytest
from skimage.metrics import structural_similarity as ssim

from main import extract_images_using_multiple_iterators
from working_with_files import get_all_files_in_dir

GIVEN_PATH = Path("data/extract_slide_from_white_background/given")
EXPECTED_PATH = Path("data/extract_slide_from_white_background/expected")


@pytest.mark.parametrize("image_path", get_all_files_in_dir(GIVEN_PATH))
def test_extract_slide_from_white_background(image_path):
    # Given
    expected_image_path = EXPECTED_PATH / image_path.name
    expected_image = cv.imread(str(expected_image_path))

    # When
    actual_image = extract_images_using_multiple_iterators(image_path)

    # Then
    assert actual_image is not None
    assert actual_image.shape == expected_image.shape

    # Convert images to grayscale for SSIM
    expected_gray = cv.cvtColor(expected_image, cv.COLOR_BGR2GRAY)
    actual_gray = cv.cvtColor(actual_image, cv.COLOR_BGR2GRAY)

    # Compare images using SSIM
    similarity_index, _ = ssim(expected_gray, actual_gray, full=True)
    assert similarity_index > 0.98
