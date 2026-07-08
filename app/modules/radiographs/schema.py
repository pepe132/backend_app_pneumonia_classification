from datetime import datetime
from typing import Literal

from pydantic import BaseModel


ImageClass = Literal[
    "covid_19",
    "normal",
    "pneumonia_bacterial",
    "pneumonia_viral",
]


class ImageProbabilities(BaseModel):
    covid_19: float
    normal: float
    pneumonia_bacterial: float
    pneumonia_viral: float


class RadiographResponse(BaseModel):
    radiograph_id: str
    evaluation_id: str
    uploaded_by: str
    original_filename: str
    content_type: str
    file_size: int
    image_class: ImageClass
    confidence: float
    probabilities: ImageProbabilities
    pneumonia_probability: float
    model_version: str
    created_at: datetime


class FusionResult(BaseModel):
    final_severity: str
    radiographic_support: Literal[
        "not_available",
        "supports_pneumonia",
        "does_not_support_pneumonia",
        "indeterminate",
        "review_required",
    ]
    concordance: Literal[
        "not_applicable",
        "concordant",
        "discordant",
        "indeterminate",
    ]
    basis: Literal["tabular_only", "clinical_and_radiographic"]
    explanation: str
    recommendation_code: str
    fusion_version: str


class RadiographAnalysisResponse(BaseModel):
    radiograph: RadiographResponse
    integrated_result: FusionResult
