import argparse, json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT/"data/raw/Indic_Climate_Stance_Expanded_1806.csv"

def audit(path=DEFAULT):
    df = pd.read_csv(path, keep_default_na=False)
    labels = df.get("stance_label", pd.Series([""]*len(df))).astype(str).str.strip()
    valid = labels.isin(["Favour","Against","None"])
    report = {
        "rows": int(len(df)), "columns": list(df.columns),
        "empty_text": int((df["text"].astype(str).str.strip()=="").sum()),
        "empty_labels": int((labels=="").sum()),
        "valid_labelled": int(valid.sum()),
        "invalid_nonempty_labels": int((~valid & (labels!="")).sum()),
        "class_distribution_labelled": labels[valid].value_counts().to_dict(),
        "origin_distribution": df["data_origin"].value_counts().to_dict() if "data_origin" in df else {},
        "language_distribution": df["detected_language"].value_counts().to_dict() if "detected_language" in df else {},
        "duplicate_text": int(df["text"].duplicated().sum()),
        "duplicate_record_id": int(df["record_id"].duplicated().sum()) if "record_id" in df else None
    }
    out = ROOT/"reports/dataset_audit.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT/"reports/dataset_audit.md").write_text(
        "# Dataset Audit\n\n```json\n"+json.dumps(report, ensure_ascii=False, indent=2)+"\n```\n",
        encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(DEFAULT))
    args=parser.parse_args()
    audit(Path(args.csv))
