import cv2

# parameters
MIN_AREA = 5
MAX_AREA = 500


def count_objects(image_path):
    """
    Count objects using contour detection
    Returns: (count, (width, height))
    """

    img = cv2.imread(str(image_path))
    if img is None:
        return 0, (0, 0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    count = 0
    for c in contours:
        area = cv2.contourArea(c)
        if MIN_AREA <= area <= MAX_AREA:
            count += 1

    h, w = img.shape[:2]
    return count, (w, h)


def generate_caption(count, size):
    """
    Generate caption based on object count and image size
    """

    w, h = size

    # image size
    if w <= 320:
        region = "small"
    elif w <= 640:
        region = "medium"
    else:
        region = "large"

    # object count
    if count == 0:
        amount = "no visible objects"
    elif count <= 3:
        amount = "a few objects"
    elif count <= 10:
        amount = "several objects"
    else:
        amount = "many objects"

    return f"A {region} image containing {amount}."