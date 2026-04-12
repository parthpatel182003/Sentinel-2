# Water Detection From Satellite Imagery

This repository is organized as a two-phase project for detecting water in remote sensing imagery.

- Phase 1 uses classical image processing on Sentinel-2 imagery.
- Phase 2 uses deep learning for semantic segmentation.
- The final stage compares both approaches to generate practical insights.

The project is designed for Google Colab and Google Drive so long-running steps can resume safely after runtime resets.

## Project Goals

1. Download satellite imagery and metadata through an API-driven workflow.
2. Build a pure image-processing baseline using spectral water indices.
3. Build a deep learning segmentation pipeline on the same study area.
4. Compare accuracy, robustness, interpretability, and compute cost.

## Recommended Dataset

- Primary imagery: Sentinel-2 Level-2A
- Optional future extension: Sentinel-1 SAR
- Label sources for Phase 2:
  - manual masks
  - JRC Global Surface Water
  - Dynamic World

## Repository Layout

```text
water-detection-remote-sensing/
|-- notebooks/
|-- src/
|-- docs/
|-- data/
|-- reports/
|-- models/
|-- requirements.txt
`-- .gitignore
```

## Notebook Flow

- `notebooks/01_download_data.ipynb`
  Downloads data, saves metadata, and builds a resumable manifest.
- `notebooks/02_preprocess_phase1.ipynb`
  Preprocesses imagery and runs classical water detection.
- `notebooks/03_data_prep_and_deep_learning.ipynb`
  Builds the training dataset and trains a segmentation model.
- `notebooks/04_compare_results.ipynb`
  Compares Phase 1 and Phase 2 outputs with metrics and visuals.

## Google Drive Layout

The shared configuration in `src/config.py` assumes a Drive root like:

```text
/content/drive/MyDrive/WaterDetectionProject/
```

Inside that root, the project will use:

- `data/raw/sentinel2`
- `data/raw/labels`
- `data/interim`
- `data/processed`
- `metadata`
- `models/checkpoints`
- `outputs`
- `reports`

## Current Status

This scaffold includes:

- project structure
- shared config
- starter notebooks
- Colab-oriented persistence strategy

The next implementation step is to build the download notebook around your chosen API and AOI.
