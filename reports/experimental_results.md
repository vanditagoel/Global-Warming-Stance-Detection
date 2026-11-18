
# Baseline Experiment Results

## 1. Model Configuration

- Model: TF-IDF word and character n-grams + class-weighted LinearSVC
- Feature extraction: Word n-grams (1–2) and character n-grams (2–5)
- Random seed: 42
- Train-test split: Stratified 80:20 split

## 2. Dataset Summary

- Total records: 1,866
- Favour: 677
- Against: 600
- None: 409
- Unlabelled records: 180
- Real records: 78
- Synthetic records: 1,788

Only records with valid stance labels were used for training.

## 3. Training and Evaluation

- Labelled rows used: 1,686
- Training rows: 1,348
- Random held-out test rows: 338
- Accuracy: 0.9704 (97.04%)
- Macro F1: 0.9686 (96.86%)

## 4. Classification Report

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Favour | 0.9565 | 0.9706 | 0.9635 |
| Against | 0.9917 | 0.9917 | 0.9917 |
| None | 0.9625 | 0.9390 | 0.9506 |

## 5. Confusion Matrix

Label order: Favour, Against, None.

| Actual / Predicted | Favour | Against | None |
|---|---:|---:|---:|
| Favour | 132 | 1 | 3 |
| Against | 1 | 119 | 0 |
| None | 5 | 0 | 77 |

## 6. Application Testing

The trained model was integrated with the FastAPI backend and React frontend.

Manual sanity checks:
- Neutral wildlife documentary comment: None
- Neutral weather comment: None
- General question about movies: None
- Video appreciation comment: None
- Explicit climate change support comment: Favour

Backend tests:
- test_root: PASSED
- test_health: PASSED
- test_feedback_validation: PASSED

Total: 3 tests passed.

## 7. Limitations

These results are not a reliable estimate of hidden-test or real-world performance.

- The random evaluation split includes synthetic records.
- Synthetic records form the majority of the dataset.
- Synthetic generation patterns may cause the model to learn artificial linguistic patterns.
- Only 78 records are real, so real-world generalisation remains uncertain.
- Manual sanity checks are not a substitute for independent evaluation.

## 8. Future Improvements

- Collect more independently annotated real Hindi and Bengali comments.
- Create a locked real-only test set.
- Perform parent-seed grouping and near-duplicate checks.
- Improve handling of neutral and context-dependent comments.
- Evaluate performance on unseen real-world comments.
