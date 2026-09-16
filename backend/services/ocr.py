import cv2
import pytesseract


# --------------------------------------------------
# TESSERACT PATH
# --------------------------------------------------

TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


pytesseract.pytesseract.tesseract_cmd = (
    TESSERACT_PATH
)


# --------------------------------------------------
# SIGN CLASSES
# --------------------------------------------------

SIGN_CLASSES = {

    "stop_sign",
    "no_entry",
    "warning_sign",
    "pedestrian_crossing",
    "speed_limit",
    "traffic_sign",
    "exit_sign",
    "sign",
    "traffic_light"

}


# --------------------------------------------------
# OCR FUNCTION
# --------------------------------------------------

def detect_text(image, detections):

    detected_texts = []


    # --------------------------------------------------
    # CHECK DETECTED OBJECTS
    # --------------------------------------------------

    for detection in detections:

        class_name = (
            detection["class_name"]
            .lower()
            .strip()
        )


        # Only process signs
        if class_name not in SIGN_CLASSES:

            continue


        # --------------------------------------------------
        # GET BOUNDING BOX
        # --------------------------------------------------

        box = detection["box"]


        x1 = max(
            0,
            int(box["x1"])
        )

        y1 = max(
            0,
            int(box["y1"])
        )

        x2 = min(
            image.shape[1],
            int(box["x2"])
        )

        y2 = min(
            image.shape[0],
            int(box["y2"])
        )


        # Invalid box
        if x2 <= x1 or y2 <= y1:

            continue


        # --------------------------------------------------
        # CROP SIGN
        # --------------------------------------------------

        sign_image = image[
            y1:y2,
            x1:x2
        ]


        if sign_image.size == 0:

            continue


        # --------------------------------------------------
        # GRAYSCALE
        # --------------------------------------------------

        gray = cv2.cvtColor(
            sign_image,
            cv2.COLOR_BGR2GRAY
        )


        # --------------------------------------------------
        # RESIZE
        # --------------------------------------------------

        gray = cv2.resize(
            gray,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )


        # --------------------------------------------------
        # NOISE REDUCTION
        # --------------------------------------------------

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )


        # --------------------------------------------------
        # THRESHOLD
        # --------------------------------------------------

        processed = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY
            + cv2.THRESH_OTSU
        )[1]


        # --------------------------------------------------
        # OCR
        # --------------------------------------------------

        text = pytesseract.image_to_string(
            processed,
            config="--psm 6"
        )


        text = text.strip()


        # --------------------------------------------------
        # CLEAN TEXT
        # --------------------------------------------------

        if text:

            text = " ".join(
                text.split()
            )

            detected_texts.append(
                text
            )


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    if detected_texts:

        return {

            "detected": True,

            "text": " ".join(
                detected_texts
            )

        }


    return {

        "detected": False,

        "text": ""

    }