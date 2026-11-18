# Methodology

1. Preserve the raw CSV and provenance columns.
2. Exclude blank/invalid labels from supervised training without deleting those rows.
3. Use word and character TF-IDF to capture lexical and noisy orthographic patterns.
4. Train a class-weighted LinearSVC baseline.
5. Evaluate on a stratified random split for initial pipeline verification.
6. Report Macro F1 as primary metric.

## Evaluation caveat
The current dataset contains 78 real and 1,728 synthetic rows. A random split may put synthetic examples in both train and test and therefore cannot establish robust generalization. A stronger study needs more independently annotated real comments and a real-only test set. Where synthetic parent relationships exist, split by parent seed group.
