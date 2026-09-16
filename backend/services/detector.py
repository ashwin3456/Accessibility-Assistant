from pathlib import Path
from ultralytics import YOLO


# --------------------------------------------------
# PATH SETTINGS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best.pt"


# --------------------------------------------------
# ACCESSIBILITY DETECTOR
# --------------------------------------------------

class AccessibilityDetector:

    def __init__(self):

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"""
YOLO model not found.

Expected location:
{MODEL_PATH}

Please train your model and copy best.pt into:
backend/models/best.pt
"""
            )

        print("Loading YOLO model...")

        self.model = YOLO(
            str(MODEL_PATH)
        )

        print("YOLO model loaded successfully.")


    # --------------------------------------------------
    # DETECT OBJECTS
    # --------------------------------------------------

    def detect(self, image):

        results = self.model(
            image,
            imgsz=640,
            conf=0.40,
            verbose=False
        )

        detections = []


        for result in results:

            if result.boxes is None:
                continue


            names = result.names


            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )


                # Bounding box
                x1, y1, x2, y2 = (
                    box.xyxy[0].tolist()
                )


                # Get class name
                class_name = names[class_id]


                detections.append({

                    "class_id": class_id,

                    "class_name": class_name,

                    "confidence": round(
                        confidence,
                        3
                    ),

                    "box": {

                        "x1": round(x1),

                        "y1": round(y1),

                        "x2": round(x2),

                        "y2": round(y2)

                    }

                })


        return detections