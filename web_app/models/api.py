from pydantic import BaseModel
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Optional, Union

class HealtcheckResponse(BaseModel):
    status: str
    app_version_hash: str
    environment: str

class InferenceRequest(BaseModel):
    nlu_model_name: str
    request_body: Optional[dict] = {}
    trace_id : str
    conversation_external_id : Optional[str] = ''

class ReviewRequest(BaseModel):
    star: int
    feedback : str
    conversation_external_id : str
    trace_id : str