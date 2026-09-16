from pathlib import Path
from ultralytics import YOLO


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = BASE_DIR / "dataset" / "dataset.yaml"

RUNS_DIR = BASE_DIR / "runs"


# --------------------------------------------------
# TRAINING
# --------------------------------------------------

def main():

    print("=" * 50)
    print("FASAL FLOW - YOLO MODEL TRAINING")
    print("=" * 50)

    # Check dataset.yaml
    if not DATASET_FILE.exists():

        print("ERROR: dataset.yaml not found.")

        print(
            f"Expected location:\n{DATASET_FILE}"
        )

        return


    print(
        f"Dataset: {DATASET_FILE}"
    )


    # --------------------------------------------------
    # LOAD PRETRAINED YOLO MODEL
    # --------------------------------------------------

    print("\nLoading YOLO model...")

    model = YOLO("yolo26n.pt")

    print("YOLO model loaded.")


    # --------------------------------------------------
    # START TRAINING
    # --------------------------------------------------

    print("\nStarting training...\n")

    model.train(

        data=str(DATASET_FILE),

        epochs=100,

        imgsz=640,

        batch=8,

        patience=20,

        project=str(RUNS_DIR),

        name="accessibility_model",

        workers=2,

        verbose=True

    )


    # --------------------------------------------------
    # TRAINING COMPLETED
    # --------------------------------------------------

    best_model = (
        RUNS_DIR
        / "accessibility_model"
        / "weights"
        / "best.pt"
    )


    print("\n" + "=" * 50)

    print("TRAINING COMPLETED")

    print("=" * 50)


    print(
        f"\nBest model:\n{best_model}"
    )


    print(
        "\nCopy best.pt to:"
    )

    print(
        BASE_DIR / "models" / "best.pt"
    )


if __name__ == "__main__":

    main()