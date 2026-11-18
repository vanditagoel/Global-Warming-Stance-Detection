
import argparse
import json
from pathlib import Path

import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    f1_score,
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Project paths
ROOT = Path(__file__).resolve().parents[1]

CSV = ROOT / "data/raw/Indic_Climate_Stance_Expanded_1806.csv"
MODEL = ROOT / "models/baseline_pipeline.joblib"
REPORTS = ROOT / "reports"

LABELS = ["Favour", "Against", "None"]


def main():

    # Command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(CSV))
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    # Load dataset
    df = pd.read_csv(args.csv, keep_default_na=False)

    df["stance_label"] = df["stance_label"].astype(str).str.strip()
    df["text"] = df["text"].astype(str)

    # Keep only valid labelled records
    df = df[
        df["stance_label"].isin(LABELS)
        & (df["text"].str.strip() != "")
    ].copy()

    if df["stance_label"].nunique() != 3:
        raise SystemExit(
            "Training requires all three labels: Favour, Against, None."
        )

    print("\nDataset distribution:")
    print(df["stance_label"].value_counts())

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["stance_label"],
        test_size=0.2,
        random_state=args.seed,
        stratify=df["stance_label"]
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # Feature extraction
    features = FeatureUnion([
        (
            "word",
            TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2),
                min_df=1,
                sublinear_tf=True,
                max_features=100000
            )
        ),
        (
            "char",
            TfidfVectorizer(
                analyzer="char",
                ngram_range=(2, 5),
                min_df=1,
                sublinear_tf=True,
                max_features=150000
            )
        )
    ])

    # Build model
    pipe = Pipeline([
        ("features", features),
        (
            "classifier",
            LinearSVC(
                class_weight="balanced",
                random_state=args.seed
            )
        )
    ])

    # Train model
    print("\nTraining model...")
    pipe.fit(X_train, y_train)

    # Predictions
    pred = pipe.predict(X_test)

    # Classification report
    report = classification_report(
        y_test,
        pred,
        labels=LABELS,
        output_dict=True,
        zero_division=0
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            pred,
            labels=LABELS,
            zero_division=0
        )
    )

    # Confusion Matrix
    cm = confusion_matrix(
        y_test,
        pred,
        labels=LABELS
    )

    print("\nConfusion Matrix:")
    print(cm)

    # Generate confusion matrix image
    REPORTS.mkdir(parents=True, exist_ok=True)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=LABELS
    )

    disp.plot(
        cmap="Blues",
        values_format="d"
    )

    plt.title("Indic Climate Stance Detection - Confusion Matrix")
    plt.tight_layout()

    confusion_path = REPORTS / "confusion_matrix.png"

    plt.savefig(
        confusion_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nConfusion matrix saved at:", confusion_path)

    # Evaluation metrics
    result = {
        "model": "TF-IDF word + character n-grams + LinearSVC",

        "evaluation_split": (
            "Stratified random split of labelled rows; "
            "includes synthetic records"
        ),

        "total_labelled_samples": len(df),
        "train_size": len(X_train),
        "test_size": len(X_test),

        "accuracy": float(
            accuracy_score(y_test, pred)
        ),

        "macro_f1": float(
            f1_score(y_test, pred, average="macro")
        ),

        "weighted_f1": float(
            f1_score(y_test, pred, average="weighted")
        ),

        "macro_precision": float(
            precision_score(
                y_test, pred,
                average="macro",
                zero_division=0
            )
        ),

        "macro_recall": float(
            recall_score(
                y_test, pred,
                average="macro",
                zero_division=0
            )
        ),

        "classification_report": report,

        "confusion_matrix": cm.tolist(),

        "labels": LABELS,

        "confusion_matrix_image": "reports/confusion_matrix.png",

        "warning": (
            "Not a real-only hidden-test estimate. "
            "Synthetic records dominate the source dataset."
        )
    }

    # Save trained model
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL)

    # Save evaluation results
    evaluation_path = REPORTS / "model_evaluation.json"

    evaluation_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("\nEvaluation Results:")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )

    print("\nModel saved at:", MODEL)
    print("Evaluation saved at:", evaluation_path)


if __name__ == "__main__":
    main()
