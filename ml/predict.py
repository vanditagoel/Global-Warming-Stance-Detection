import argparse, joblib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("--model",default=str(ROOT/"models/baseline_pipeline.joblib"))
    a=p.parse_args()
    model=joblib.load(a.model)
    print(model.predict([a.text])[0])
if __name__=="__main__": main()
