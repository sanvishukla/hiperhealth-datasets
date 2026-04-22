from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class DatasetMetadata(BaseModel):
    name: str = Field(..., description="Name of the dataset (e.g., ISIC 2020)")
    source: str = Field("", description="Source of the dataset (e.g., WHO, specific hospital)")
    target_skill: str = Field(..., description="The clinical domain (e.g., skin, eye, ear)")
    modality: str = Field("", description="Data type (e.g., dermoscopy images, retina scans)")
    access_link: HttpUrl = Field(..., description="Direct download URL, HuggingFace path, or Kaggle link")
    licensing: str = Field("", description="The open-source or usage license (e.g., MIT, CC BY 4.0)")
    description: str = Field("", description="A brief summary of what the data contains")
    size: str = Field("", description="Approximate file size or number of samples")
