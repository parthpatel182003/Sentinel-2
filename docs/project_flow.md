# Project Flow

## Problem Statement

Detect water from satellite imagery in two stages:

1. classical image processing only
2. deep learning segmentation

Then compare both approaches to understand where each method works best.

## Dataset Strategy

### Primary Dataset

- Sentinel-2 Level-2A

Reason:

- high-value spectral bands for water detection
- suitable for index-based methods
- suitable for patch-based deep learning

### Optional Future Dataset

- Sentinel-1 SAR

Reason:

- robust under cloud cover
- useful when optical imagery is unreliable

### Label Options For Deep Learning

- manual polygon-to-mask workflow
- JRC Global Surface Water
- Dynamic World

## End-To-End Flow

### Notebook 1: Download Data

Goal:

- define area of interest
- define time range
- query imagery API
- filter scenes by cloud cover
- save raw assets and manifest files to Drive

Outputs:

- scene manifest CSV
- downloaded scene folders
- metadata log

### Notebook 2: Preprocess And Phase 1

Goal:

- standardize required bands
- compute water indices
- produce water masks using image-processing rules

Core methods:

- NDWI
- MNDWI
- thresholding
- morphology
- connected component filtering

Outputs:

- processed band stacks
- index rasters
- water masks
- visual overlays
- area summaries

### Notebook 3: Data Preparation And Deep Learning

Goal:

- prepare training labels
- tile scenes into patches
- split train, validation, and test sets
- train a segmentation model

Starter model:

- U-Net

Outputs:

- patch dataset
- checkpoints
- prediction masks
- training logs

### Notebook 4: Compare Results

Goal:

- compare classical and deep learning outputs on the same test scenes

Metrics:

- IoU
- Dice
- Precision
- Recall
- water area difference

Analysis:

- failure cases
- cloud and shadow sensitivity
- shoreline quality
- compute time
- explainability

## Colab Design Rules

- mount Google Drive at the beginning of every notebook
- keep all important outputs on Drive
- make steps rerunnable without re-downloading data
- write manifest and log files after every major stage
- save checkpoints every epoch during training
- process data scene-by-scene where possible

## Proposed Build Order

1. finalize AOI and time range
2. implement download notebook
3. implement preprocessing and Phase 1 baseline
4. define label strategy
5. implement patch creation and training
6. implement evaluation notebook
7. generate final report visuals

