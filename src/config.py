from pathlib import Path


# Update this if you want a different root folder in Google Drive.
DRIVE_ROOT = Path("/content/drive/MyDrive/WaterDetectionProject")


PATHS = {
    "data_root": DRIVE_ROOT / "data",
    "raw_root": DRIVE_ROOT / "data" / "raw",
    "raw_sentinel2": DRIVE_ROOT / "data" / "raw" / "sentinel2",
    "raw_labels": DRIVE_ROOT / "data" / "raw" / "labels",
    "interim_root": DRIVE_ROOT / "data" / "interim",
    "processed_root": DRIVE_ROOT / "data" / "processed",
    "patches_root": DRIVE_ROOT / "data" / "processed" / "patches",
    "metadata_root": DRIVE_ROOT / "metadata",
    "models_root": DRIVE_ROOT / "models",
    "checkpoints_root": DRIVE_ROOT / "models" / "checkpoints",
    "exported_models_root": DRIVE_ROOT / "models" / "exported",
    "outputs_root": DRIVE_ROOT / "outputs",
    "figures_root": DRIVE_ROOT / "outputs" / "figures",
    "masks_root": DRIVE_ROOT / "outputs" / "masks",
    "overlays_root": DRIVE_ROOT / "outputs" / "overlays",
    "reports_root": DRIVE_ROOT / "reports",
}


PROJECT_CONFIG = {
    "project_name": "water-detection-remote-sensing",
    "dataset_name": "sentinel-2-l2a",
    "aoi_name": "replace_with_aoi_name",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "max_cloud_cover": 20,
    "phase1_indices": ["NDWI", "MNDWI"],
    "phase2_model_name": "unet",
    "patch_size": 256,
    "patch_stride": 256,
    "batch_size": 8,
    "num_epochs": 20,
    "learning_rate": 1e-3,
    "random_seed": 42,
}


def ensure_project_dirs() -> None:
    for path in PATHS.values():
        path.mkdir(parents=True, exist_ok=True)


def manifest_path(name: str) -> Path:
    return PATHS["metadata_root"] / f"{name}.csv"

