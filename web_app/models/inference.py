from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Optional, Union

class InferenceRequest(BaseModel):
    nlu_model_name: str
    request_body: Optional[dict] = {}
    trace_id : str