from web_app.logs import LOG
from web_app.database import orm_session, Model
from web_app.models.nlu import NLUModels, NLUModelConfig
import os

try:
    from web_app.core.nlu import OpenAIRAG
except Exception as e:
    LOG.warning(f'error import FastTextSearchServiceModel {e}', exc_info=False)
    OpenAIRAG = None

class Models:
    OpenAIRAG = OpenAIRAG

class ModelLoader:
    def __init__(self, active_model_agg={'is_active': True}) -> None:
        self.active_models = orm_session.query(
            Model).filter_by(**active_model_agg).all()

    def load_model_config(self) -> NLUModels:
        """
        Load model class that get from db
        this method will be initiate when app first run
        to handle large model loaded
        """
        nlu_models = []
        for row in self.active_models:
            class_name = row.class_name
            model_arg = row.model_arg

            # load object model
            modelclass = getattr(Models, class_name)
            LOG.info(f'load model row {row.id} {class_name} {model_arg} {modelclass}')
            modelclass = modelclass(**model_arg)

            nlu_models.append(NLUModelConfig(
                name=row.name,
                class_name=class_name,
                description=row.description,
                model_arg=row.model_arg,
                nlumodel_class=modelclass,
                nlumodel_id=row.id
            ))

        nlu_models = NLUModels(models=nlu_models)

        LOG.info(f'all models config loaded {nlu_models.model_dump()}')
        return nlu_models