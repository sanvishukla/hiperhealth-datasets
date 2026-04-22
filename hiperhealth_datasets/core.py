import os
import json
from pathlib import Path
from typing import List, Optional
from .models import DatasetMetadata

# Find the root repository path by going up from this file's location
# hiperhealth_datasets/core.py -> hiperhealth_datasets -> root
ROOT_DIR = Path(__file__).parent.parent
REGISTRY_DIR = ROOT_DIR / "registry"

def _get_registry_files() -> List[Path]:
    """Return a list of all json files inside the registry directory."""
    if not REGISTRY_DIR.exists():
        return []
    
    files = []
    # registry layout: registry/<skill>/<dataset>.json
    for skill_dir in REGISTRY_DIR.iterdir():
        if skill_dir.is_dir():
            for filepath in skill_dir.glob("*.json"):
                files.append(filepath)
    return files

def get_datasets(skill: Optional[str] = None, license: Optional[str] = None) -> List[DatasetMetadata]:
    """
    Fetch and filter datasets based on target skill and licensing.
    """
    results = []
    for filepath in _get_registry_files():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                dataset = DatasetMetadata(**data)
                
                # Apply filters
                if skill and dataset.target_skill.lower() != skill.lower():
                    continue
                if license and dataset.licensing.lower() != license.lower():
                    continue
                    
                results.append(dataset)
        except Exception as e:
            print(f"Warning: Failed to load or parse {filepath}: {e}")
            
    return results

def get_dataset(name: str) -> Optional[DatasetMetadata]:
    """Retrieve a single dataset by its exact name."""
    for filepath in _get_registry_files():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                dataset = DatasetMetadata(**data)
                if dataset.name.lower() == name.lower():
                    return dataset
        except Exception:
            continue
    return None

def add_dataset(dataset: DatasetMetadata) -> Path:
    """Save a DatasetMetadata object into the local registry."""
    # Ensure skill directory exists
    skill_dir = REGISTRY_DIR / dataset.target_skill.lower()
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename from dataset name 
    safe_name = "".join([c if c.isalnum() else "_" for c in dataset.name.lower()])
    filepath = skill_dir / f"{safe_name}.json"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Pydantic v2
        json_data = dataset.model_dump_json(indent=4)
        f.write(json_data)
        
    return filepath
