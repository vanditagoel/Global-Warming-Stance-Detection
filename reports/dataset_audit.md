# Dataset audit

{
  "rows": 1806,
  "columns": [
    "record_id",
    "comment_id",
    "synthetic_id",
    "video_id",
    "text",
    "detected_language",
    "stance_label",
    "confidence",
    "data_origin",
    "parent_seed_id",
    "source_platform",
    "annotator_id",
    "annotation_confidence"
  ],
  "label_distribution_including_blank": {
    "Favour": 650,
    "Against": 598,
    "": 426,
    "None": 132
  },
  "origin_distribution": {
    "Synthetic": 1728,
    "Real": 78
  },
  "language_distribution": {
    "hi": 520,
    "bn": 487,
    "hi-en": 439,
    "bn-en": 359,
    "en": 1
  },
  "empty_text": 0,
  "duplicate_text": 0,
  "duplicate_record_id": 0,
  "note": "Blank stance labels are preserved in raw data and excluded from supervised training."
}
