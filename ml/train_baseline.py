import argparse, json, os
from pathlib import Path
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT/"data/raw/Indic_Climate_Stance_Expanded_1806.csv"
MODEL = ROOT/"models/baseline_pipeline.joblib"

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(CSV))
    parser.add_argument("--seed", type=int, default=42)
    args=parser.parse_args()
    df=pd.read_csv(args.csv, keep_default_na=False)
    df["stance_label"]=df["stance_label"].astype(str).str.strip()
    df["text"]=df["text"].astype(str)
    df=df[df["stance_label"].isin(["Favour","Against","None"]) & (df["text"].str.strip()!="")].copy()
    if df["stance_label"].nunique()!=3:
        raise SystemExit("Training requires all three labels: Favour, Against, None.")
    X_train,X_test,y_train,y_test=train_test_split(
        df["text"],df["stance_label"],test_size=0.2,random_state=args.seed,stratify=df["stance_label"])
    features=FeatureUnion([
        ("word",TfidfVectorizer(analyzer="word",ngram_range=(1,2),min_df=1,sublinear_tf=True,max_features=100000)),
        ("char",TfidfVectorizer(analyzer="char",ngram_range=(2,5),min_df=1,sublinear_tf=True,max_features=150000))
    ])
    pipe=Pipeline([("features",features),("classifier",LinearSVC(class_weight="balanced",random_state=args.seed))])
    pipe.fit(X_train,y_train)
    pred=pipe.predict(X_test)
    report=classification_report(y_test,pred,labels=["Favour","Against","None"],output_dict=True,zero_division=0)
    result={
        "model":"TF-IDF word+character n-grams + LinearSVC",
        "evaluation_split":"stratified random split of labelled rows; includes synthetic records",
        "train_size":len(X_train),"test_size":len(X_test),
        "accuracy":float(accuracy_score(y_test,pred)),
        "macro_f1":float(f1_score(y_test,pred,average="macro")),
        "classification_report":report,
        "confusion_matrix":confusion_matrix(y_test,pred,labels=["Favour","Against","None"]).tolist(),
        "labels":["Favour","Against","None"],
        "warning":"Not a real-only hidden-test estimate. Synthetic records dominate the source dataset."
    }
    MODEL.parent.mkdir(exist_ok=True)
    joblib.dump(pipe,MODEL)
    (ROOT/"reports/model_evaluation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
