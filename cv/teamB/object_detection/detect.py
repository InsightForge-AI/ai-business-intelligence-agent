import cv2

# parameters
MIN_AREA = 5
MAX_AREA = 500


def detect_objects(image_path):
    """
    Detect objects using contour detection
    Returns: list of bounding boxes
    """

    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read: {image_path}")

    # grayscale + blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # threshold
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if MIN_AREA <= area <= MAX_AREA:
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append({
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            })

    return detections