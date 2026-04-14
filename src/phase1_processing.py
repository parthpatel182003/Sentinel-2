import numpy as np
import rasterio
import cv2
import os
import matplotlib.pyplot as plt


def load_sentinel_image(path):
    with rasterio.open(path) as src:
        return {
            "blue": src.read(1),
            "green": src.read(2),
            "red": src.read(3),
            "nir": src.read(4),
            "swir": src.read(5),
            "meta": src.meta
        }


def compute_indices(bands):
    green = bands["green"].astype(np.float32)
    nir = bands["nir"].astype(np.float32)
    swir = bands["swir"].astype(np.float32)

    ndwi = (green - nir) / (green + nir + 1e-6)
    mndwi = (green - swir) / (green + swir + 1e-6)

    return ndwi, mndwi


def otsu_threshold(image):
    image = np.nan_to_num(image)

    image_norm = (image - image.min()) / (image.max() - image.min() + 1e-6)
    image_8bit = (image_norm * 255).astype(np.uint8)

    _, thresh = cv2.threshold(
        image_8bit, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Slight smoothing
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return thresh


def remove_small_components(mask):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)

    clean_mask = np.zeros_like(mask)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        width = stats[i, cv2.CC_STAT_WIDTH]
        height = stats[i, cv2.CC_STAT_HEIGHT]

        aspect_ratio = max(width, height) / (min(width, height) + 1e-6)

        # 🔥 FINAL FILTER
        if area > 300 and aspect_ratio < 5:
            clean_mask[labels == i] = 255

    return clean_mask


def remove_ocean_largest_component(mask):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)

    largest_label = 1
    largest_area = 0

    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > largest_area:
            largest_area = stats[i, cv2.CC_STAT_AREA]
            largest_label = i

    mask[labels == largest_label] = 0

    return mask


def save_mask(mask, meta, output_path):
    meta.update({
        "count": 1,
        "dtype": "uint8"
    })

    with rasterio.open(output_path, "w", **meta) as dst:
        dst.write(mask, 1)


def create_overlay(red, green, blue, mask, output_path):
    rgb = np.stack([red, green, blue], axis=-1)
    rgb = (rgb / (np.max(rgb) + 1e-6) * 255).astype(np.uint8)

    overlay = rgb.copy()
    overlay[mask == 255] = [255, 0, 0]

    plt.imshow(overlay)
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()


def process_image(image_path, mask_dir, overlay_dir):
    name = os.path.basename(image_path).replace(".tif", "")

    bands = load_sentinel_image(image_path)
    _, mndwi = compute_indices(bands)

    mask = otsu_threshold(mndwi)

    mask = remove_small_components(mask)

    mask = remove_ocean_largest_component(mask)

    mask_path = os.path.join(mask_dir, f"{name}_water_mask_mndwi.tif")
    overlay_path = os.path.join(overlay_dir, f"{name}_water_overlay.png")

    save_mask(mask, bands["meta"], mask_path)
    create_overlay(
        bands["red"], bands["green"], bands["blue"],
        mask, overlay_path
    )

    water_pixels = np.sum(mask == 255)
    total_pixels = mask.size

    return {
        "image": name,
        "water_pixels": int(water_pixels),
        "water_ratio": float(water_pixels / total_pixels)
    }
