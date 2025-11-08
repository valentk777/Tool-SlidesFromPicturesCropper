import cv2 as cv

from paths import SLIDES_PATH, RESULT_PATH
from working_with_files import get_all_files_in_dir, check_for_duplicates_and_remove_if_exist


def show_image(_image):
    cv.imshow("Image", _image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def resize_card(_image):
    scale_percent = 27  # percent of original size
    width = int(_image.shape[1] * scale_percent / 100)
    height = int(_image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv.resize(_image, dim, interpolation=cv.INTER_AREA)


def is_a_shape_of_expected_card_size(w):
    return 490 < w < 500


def detected_cards_generator(_image):
    img = cv.imread(str(_image))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 250, 255, 0, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, 1, 2)

    for idx, cnt in enumerate(contours):
        x1, y1 = cnt[0][0]
        approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)

        if len(approx) != 4:
            continue

        x, y, w, h = cv.boundingRect(cnt)

        if not is_a_shape_of_expected_card_size(w):
            continue

        actual_card = img[y:y + h, x:x + w]
        yield actual_card

        # additionally pain rectangle on original image to manually check if all rectangles detected.
        cv.putText(img, 'Rectangle', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        img = cv.drawContours(img, [cnt], -1, (0, 255, 0), 3)


def save_image(_image, name=""):
    cv.imwrite(str(RESULT_PATH / f"{name}.jpg"), _image)


if __name__ == "__main__":
    images = get_all_files_in_dir(SLIDES_PATH)
    image_number = 0

    for image in images:
        for detected in detected_cards_generator(image):
            resized = resize_card(detected)
            save_image(resized, str(image_number))
            image_number += 1

    check_for_duplicates_and_remove_if_exist(RESULT_PATH)
