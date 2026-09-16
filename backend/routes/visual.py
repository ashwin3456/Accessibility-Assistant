from fastapi import APIRouter, UploadFile, File, HTTPException

import cv2
import numpy as np

from services.detector import AccessibilityDetector
from services.obstacle_detector import analyze_detections
from services.ocr import detect_text


router = APIRouter(
    prefix="/api/visual",
    tags=["Visual Assistance"]
)


# --------------------------------------------------
# LOAD YOLO MODEL
# --------------------------------------------------

try:
    detector = AccessibilityDetector()
    MODEL_LOADED = True

except Exception as e:
    detector = None
    MODEL_LOADED = False

    print("======================================")
    print("WARNING: YOLO MODEL NOT LOADED")
    print("Reason:", e)
    print("Place trained best.pt inside:")
    print("backend/models/best.pt")
    print("======================================")


# --------------------------------------------------
# MODEL STATUS
# --------------------------------------------------

@router.get("/status")
def visual_status():

    if not MODEL_LOADED:

        return {
            "status": "error",
            "model_loaded": False,
            "message": "YOLO model is not loaded"
        }

    return {
        "status": "ready",
        "model_loaded": True,
        "message": "Visual AI model is ready"
    }


# --------------------------------------------------
# OBJECT / OBSTACLE / SIGN DETECTION
# --------------------------------------------------

@router.post("/detect")
async def detect_objects(
    file: UploadFile = File(...)
):

    # Check model
    if detector is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "YOLO model is not loaded. "
                "Train the model and place best.pt "
                "inside backend/models/"
            )
        )


    try:

        # ------------------------------------------
        # READ IMAGE
        # ------------------------------------------

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="Empty image received"
            )


        # ------------------------------------------
        # CONVERT IMAGE TO NUMPY
        # ------------------------------------------

        image_array = np.frombuffer(
            contents,
            dtype=np.uint8
        )


        # ------------------------------------------
        # DECODE IMAGE
        # ------------------------------------------

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )


        if image is None:

            raise HTTPException(
                status_code=400,
                detail="Invalid image file"
            )


        # ------------------------------------------
        # YOLO DETECTION
        # ------------------------------------------

        detections = detector.detect(
            image
        )


        # ------------------------------------------
        # ANALYZE OBJECTS
        # ------------------------------------------

        analysis = analyze_detections(
            detections
        )


        # ------------------------------------------
        # OCR FOR SIGN TEXT
        # ------------------------------------------

        try:

            text_result = detect_text(
                image,
                detections
            )

        except Exception as ocr_error:

            print(
                "OCR error:",
                ocr_error
            )

            text_result = {
                "detected": False,
                "text": "",
                "error": str(ocr_error)
            }


        # ------------------------------------------
        # RESPONSE
        # ------------------------------------------

        return {

            "success": True,

            "detections": detections,

            "analysis": analysis,

            "ocr": text_result

        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "Visual detection error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )