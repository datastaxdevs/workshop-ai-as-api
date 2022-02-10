from pydantic import BaseModel
from typing import Optional, List, Dict

# request models

class SingleTextQuery(BaseModel):
    text: str
    echo_input: bool = False
    skip_cache: bool = False


class MultipleTextQuery(BaseModel):
    texts: List[str]
    echo_input: bool = True
    skip_cache: bool = False


# response models

class APIInfo(BaseModel):
    api_name: str
    astra_db_keyspace: str
    caller_id: str
    model_directory: str
    model_version: str
    started_at: str


class PredictionTopInfo(BaseModel):
    label: str
    value: float


class PredictionResult(BaseModel):
    input: Optional[str]
    prediction: Dict[str, float]
    top: PredictionTopInfo
    from_cache: bool


class CallerLogEntry(BaseModel):
    index: int
    input: str
    called_at: str
