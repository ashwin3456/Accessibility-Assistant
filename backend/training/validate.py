from pathlib import Path
from ultralytics import YOLO


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best.pt"

DATASET_FILE = BASE_DIR / "dataset" / "dataset.yaml"


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

def main():

    print("=" * 50)
    print("FASAL FLOW - MODEL VALIDATION")
    print("=" * 50)


    # --------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------

    if not MODEL_PATH.exists():

        print("\nERROR: best.pt not found.")

        print(
            f"\nExpected location:\n{MODEL_PATH}"
        )

        print(
            "\nTrain the model first using:"
        )

        print(
            "python training\\train.py"
        )

        return


    # --------------------------------------------------
    # CHECK DATASET
    # --------------------------------------------------

    if not DATASET_FILE.exists():

        print("\nERROR: dataset.yaml not found.")

        print(
            f"\nExpected location:\n{DATASET_FILE}"
        )

        return


    # --------------------------------------------------
    # LOAD TRAINED MODEL
    # --------------------------------------------------

    print("\nLoading trained model...")

    model = YOLO(
        str(MODEL_PATH)
    )

    print("Model loaded successfully.")


    # --------------------------------------------------
    # VALIDATE
    # --------------------------------------------------

    print("\nRunning validation...\n")

    results = model.val(

        data=str(DATASET_FILE),

        imgsz=640,

        batch=8,

        workers=2

    )


    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n" + "=" * 50)

    print("VALIDATION COMPLETED")

    print("=" * 50)


    try:

        print(
            f"\nmAP50: {results.box.map50:.4f}"
        )

        print(
            f"mAP50-95: {results.box.map:.4f}"
        )

    except Exception:

        print(
            "\nValidation completed."
        )


if __name__ == "__main__":

    main()