# HiperHealth Dataset Registry

This package holds the metadata registry of datasets tailored for fine-tuning medical skills within the **HiperHealth** ecosystem. Designed to be modular and community-driven, it uses a minimal JSON-based Git hierarchy to list datasets according to clinical domains (e.g., `skin`, `eye`).

## Installation

You can install this directory as a library:

```bash
pip install -e .
```

## Python API

You can programmatically fetch registered datasets for training loops:

```python
from hiperhealth_datasets import get_datasets, get_dataset

# Fetch all CC-licensed skin images
skin_datasets = get_datasets(skill="skin", license="CC BY 4.0")

for ds in skin_datasets:
    print(ds.name, ds.access_link)
```

## CLI Usage

This registry ships with the `hdatasets` CLI for easy local management.

- **List datasets**:
  ```bash
  hdatasets list
  hdatasets list --skill skin
  ```
- **Add a new dataset** interactively:
  ```bash
  hdatasets add
  ```
- **Validate** the registry metadata schema:
  ```bash
  hdatasets validate
  ```

## Available Datasets

<!-- DATASETS_START -->

### Eye

| Name | Source | Modality | Size | License | Link |
|---|---|---|---|---|---|
| ISIC | ISIC | Images | 200 | 2 | [Link](https://challenge.isic-archive.com/data/#milk10k) |

### Skin

| Name | Source | Modality | Size | License | Link |
|---|---|---|---|---|---|
| ISIC MILK10K | ISIC | Dermoscopy Images | 10k+ images, 5240 lesions |  | [Link](https://challenge.isic-archive.com/data/#milk10k) |

<!-- DATASETS_END -->

## Submitting New Datasets via GitHub Issues

You don't need to manually draft JSON files! We leverage GitHub actions to parse issue templates and automatically generate Pull Requests.

1. Create a `New Issue`.
2. Select the **Submit a Dataset** template.
3. Fill out the specific diagnostic details (Name, Target Skill, Link, License, Size, etc.).
4. Submit the issue! A GitHub action will parse the input, commit a validated JSON to the `registry/` folder under your specified skill, and open a Pull Request for our maintainers to review.

### Metadata Schema

Every dataset is strictly modeled by the following properties:
- `Name`: e.g., ISIC 2020
- `Source`: e.g., WHO
- `Target Skill`: e.g., skin, ear, eye
- `Modality`: e.g., dermoscopy images
- `Access Link`: An HTTP URL to download/view the dataset
- `Licensing`: e.g., CC BY 4.0
- `Description`: Dataset summary
- `Size`: Approximate file size or file count