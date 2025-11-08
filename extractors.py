from pathlib import Path

import cv2 as cv
import numpy as np


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def perspective_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def extract_slide_from_white_background(_image_path: Path):
    img = cv.imread(str(_image_path))
    h, w, _ = img.shape

    # Define the color range for white
    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255])

    # Create a mask for the white color
    mask = cv.inRange(img, lower_white, upper_white)

    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Find the largest contour
    largest_contour = max(contours, key=cv.contourArea)

    # Get the bounding box of the contour
    x_contour, y_contour, w_contour, h_contour = cv.boundingRect(largest_contour)

    # Check if the contour is large enough
    if w_contour > 0.5 * w or h_contour > 0.5 * h:
        # Get the minimum area rectangle
        rect = cv.minAreaRect(largest_contour)
        box = cv.boxPoints(rect)
        box = np.intp(box)

        # Crop and de-skew the slide
        warped = perspective_transform(img, box.astype("float32"))
        return warped

    return None
