# Global Warming Stance Detection

## Project Overview
This project focuses on multilingual climate stance classification. It classifies social media comments related to the claim:

**"Climate change and global warming is a serious concern."**

The model predicts three stance categories:
- **Favour** – Comments supporting the claim.
- **Against** – Comments opposing the claim.
- **None** – Neutral or unrelated comments.

## Dataset Description
The dataset contains Hindi, Bengali, and code-mixed comments.

- Total records: 1,806
- Favour: 650
- Against: 598
- None: 332
- Unlabelled records: 226
- Real records: 78
- Synthetic records: 1,728

Unlabelled records are excluded from model training. Synthetic examples are AI-generated and have not been independently human-verified.

## Methodology
The project uses a machine learning pipeline consisting of:

1. Data loading and preprocessing.
2. Removal of unlabelled and empty-text records.
3. Text feature extraction using TF-IDF.
4. Word-level n-grams (1–2).
5. Character-level n-grams (3–5).
6. Classification using Linear Support Vector Machine (Linear SVM).

## Model Evaluation
The labelled dataset was divided into 80% training and 20% testing using stratified sampling.

| Metric | Result |
|---|---:|
| Accuracy | 99.37% |
| Macro F1-score | 99.47% |
| Training samples | 1,264 |
| Testing samples | 316 |

These are preliminary results from a random split. The test set contains only 9 real comments and 307 synthetic comments, so the results should not be interpreted as evidence of equivalent real-world performance.

## Repository Files
- `CSET346_Indic_Climate_Stance.ipynb` – Implementation and experiments.
- `Indic_Climate_Stance_Expanded_1806_FIXED.csv` – Dataset.
- `climate_stance_model.pkl` – Trained classification model.

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Matplotlib
- TF-IDF
- Linear SVM
- Google Colab

## Future Work
- Collect more real-world labelled comments.
- Improve Hindi and Bengali language coverage.
- Evaluate model generalisation on an independent real-world test set.
- Improve handling of sarcasm and code-mixed language.

## Conclusion
The project demonstrates a multilingual machine learning approach for climate stance classification using TF-IDF features and Linear SVM.
