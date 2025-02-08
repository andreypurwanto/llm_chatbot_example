from datetime import date, datetime, time, timedelta
from typing import List, Union, Optional
from pydantic import BaseModel as PydanticBaseModel
import typing

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class NLUModelConfig(BaseModel):
    nlumodel_id: int
    name: str
    class_name: str
    description: str
    model_arg: dict
    nlumodel_class: typing.Any

class NLUModels(BaseModel):
    models: List[NLUModelConfig]