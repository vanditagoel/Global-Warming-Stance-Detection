\"\"\"Optional transformer training entry point.

This is deliberately a documented extension point rather than a fake trainer.
Install transformers, datasets, and torch; prepare a reviewed, leakage-safe
training split before implementing/fitting a chosen Indic-capable checkpoint.
The baseline pipeline is the runnable low-resource reference model.
\"\"\"
def main():
    raise SystemExit(
        "Transformer training is optional and not implemented in this baseline package. "
        "Choose and verify an Indic-capable checkpoint, then implement a reproducible "
        "Trainer workflow with a real-only held-out test set. See README."
    )
if __name__ == "__main__": main()
