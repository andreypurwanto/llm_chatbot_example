from web_app.models.nlu import NLUModels, NLUModelConfig
from typing import Union
from web_app.logs import LOG

def filter_model_config(nlu_models : NLUModels, nlumodel_name : str) -> Union[NLUModelConfig, None]:
    for model_config in nlu_models.models:
        if model_config.name == nlumodel_name:
            return model_config
    
    return None