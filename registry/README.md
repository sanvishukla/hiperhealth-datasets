# Dataset Registry

This folder contains the metadata for all datasets indexed by the HiperHealth library. The architecture is minimal and designed for easy Git collaboration:
- Directory names dictate the target **skill** (e.g., `skin`, `eye`).
- Inner JSON files (e.g., `isic2020.json`) dictate individual dataset metadata.

## Schema
Datasets must adhere to the `DatasetMetadata` Pydantic model found in the package:
- name
- source
- target_skill
- modality
- access_link
- licensing
- description
- size
