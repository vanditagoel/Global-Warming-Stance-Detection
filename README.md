# Indic Climate Stance Challenge

A reproducible research application for classifying Hindi and Bengali social-media comments toward the claim:

**"Climate change and global warming is a serious concern."**

The application classifies comments into three stance categories: `Favour`, `Against`, and `None`.

## Features

- React + Vite + TypeScript frontend.
- FastAPI backend with single and batch inference.
- TF-IDF word and character n-grams with a LinearSVC baseline classifier.
- SQLite prediction history and user feedback.
- Dataset auditing and reproducible training/evaluation scripts.
- CSV batch upload and export.
- Real and synthetic data provenance retained.

## Dataset Audit

The updated dataset contains **1,866 records and 13 columns**.

| Dataset property | Count |
|---|---:|
| Total records | 1,866 |
| Real records | 78 |
| Synthetic records | 1,788 |
| Favour | 677 |
| Against | 600 |
| None | 409 |
| Unlabelled | 180 |

Only records with valid labels from the three-class schema are used for supervised training.

Synthetic examples are retained with provenance information and are not represented as human annotations. The dataset is predominantly synthetic, which is an important limitation for model evaluation and real-world generalisation.

## Quick Start

### 1. Requirements

- Python 3.10+
- Node.js 18+
- npm

### 2. Backend Setup

Open a terminal in the project root directory.

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

Install dependencies and prepare the model:

```bash
pip install -r requirements.txt
python ml/dataset_audit.py
python ml/train_baseline.py
```

Start the backend:

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally:

http://localhost:5173

The frontend expects the API at:

http://127.0.0.1:8000

Set `VITE_API_URL` if a different backend URL is required.

## Training and Evaluation

### Model Configuration

The baseline model uses:

- Word TF-IDF n-grams: (1, 2)
- Character TF-IDF n-grams: (2, 5)
- Class-weighted LinearSVC classifier.
- Stratified 80:20 train-test split.
- Random seed: 42.

Run training and evaluation:

```bash
python ml/dataset_audit.py
python ml/train_baseline.py
```

### Latest Evaluation Results

| Metric | Result |
|---|---:|
| Labelled rows | 1,686 |
| Training rows | 1,348 |
| Test rows | 338 |
| Accuracy | 97.04% |
| Macro F1 | 96.86% |

### Class-wise Performance

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Favour | 95.65% | 97.06% | 96.35% |
| Against | 99.17% | 99.17% | 99.17% |
| None | 96.25% | 93.90% | 95.06% |

### Confusion Matrix

Label order: Favour, Against, None.

| Actual / Predicted | Favour | Against | None |
|---|---:|---:|---:|
| Favour | 132 | 1 | 3 |
| Against | 1 | 119 | 0 |
| None | 5 | 0 | 77 |

**Research caution:** These evaluation results include synthetic records and are not a reliable estimate of hidden-test or real-world performance. Synthetic generation patterns may inflate evaluation scores.

A locked, independently annotated real-only test set is needed to assess generalisation.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Project status |
| GET | `/health` | Model status |
| POST | `/predict` | Single-comment prediction |
| POST | `/predict/batch` | Batch predictions |
| POST | `/explain` | Influential TF-IDF features |
| GET | `/model-info` | Model metadata |
| GET | `/analytics` | Dataset and prediction analytics |
| GET | `/history` | Prediction history |
| POST | `/feedback` | Corrected-label feedback |

### Example API Request

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"जलवायु परिवर्तन बहुत गंभीर समस्या है"}'
```

## Project Structure

```text
backend/       FastAPI app, routes, database, services, tests
frontend/      React + Vite application
ml/            Dataset audit, training, evaluation, inference
data/raw/      Source dataset
data/processed/Generated audit outputs
models/        Trained model bundle
reports/       Dataset and model evaluation reports
scripts/       Helper scripts
```

## Reproducibility

The training script uses random seed 42 by default. A different seed can be supplied using the `--seed` argument.

Example:

```bash
python ml/train_baseline.py --seed 42
```

Training and inference share the saved scikit-learn pipeline.

The saved model uses Python pickle/joblib. Only load model files that you created or trust.

Keep the original source dataset unchanged when conducting reproducible experiments.

## Testing

Run backend tests using:

```bash
PYTHONPATH=. python -m pytest backend/tests -v
```

Latest test results:

- `test_root`: PASSED
- `test_health`: PASSED
- `test_feedback_validation`: PASSED

**Total: 3 tests passed.**

## Limitations

- Stance labels are task-specific and require careful annotation.
- Synthetic examples can inflate validation performance and differ from real-world comments.
- The dataset contains substantially more synthetic than real records.
- Language tags are inherited from the dataset; no independent language-identification model is included.
- LinearSVC scores are transformed into relative normalized scores for display. They are not calibrated probabilities.
- Explanations show influential TF-IDF features, not causal explanations.
- More independently annotated Hindi, Bengali and code-mixed comments are required for reliable generalisation.

## GitHub Setup

After creating a GitHub repository, use:

```bash
git init
git add .
git commit -m "Initial Indic Climate Stance Challenge implementation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/indic-climate-stance-challenge.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

Add team members as collaborators through GitHub Settings → Collaborators.

## License

Choose a license only after confirming the source dataset's redistribution permissions.
