from web_app.models.api import InferenceRequest
from web_app.utils.helper import filter_model_config
from web_app.base.model_loader import ModelLoader
from web_app.models.nlu import NLUModelConfig
from typing import Union
from web_app.logs import LOG
from fastapi import HTTPException, status
from web_app.base.loader import model_configs
from web_app.database import orm_session, Chat, Conversation, LLMResult
import functools

def get_active_model_configs():
    res = []
    for model in model_configs.models:
        temp_ = model.model_dump().copy()
        if 'nlumodel_class' in temp_:
            del temp_['nlumodel_class']  
        res.append(temp_)
    return res

class Inference:
    def __init__(self, inference_request: InferenceRequest, model_configs=model_configs):
        self.inference_request = inference_request
        self.model_config = model_configs
        self.conversation = None
        self.chat = None
        self.result_metadata = None
    
    def __insert_conversation(self):
        conv_obj = orm_session.query(Conversation).filter(Conversation.external_id == self.inference_request.conversation_external_id).first()
           
        if not conv_obj:
            conv_obj = Conversation(
                model_id = self.nlu_model.nlumodel_id,
                user_id = 'a', # TODO adjust
                external_id = self.inference_request.conversation_external_id
            )
            orm_session.add(conv_obj)
        orm_session.commit()
        self.conversation = conv_obj
    
    def __insert_chat(self):
        chat_obj = Chat(
            conversation_id = self.conversation.id,
            query = self.inference_request.request_body.get('query'),
        )
        orm_session.add(chat_obj)
        orm_session.commit()
        self.chat = chat_obj
    
    def __insert_llm_result(self):
        if not self.nlu_model:
            raise Exception('invalid nlu model')
        
        llm_obj = LLMResult(
            chat_id = self.chat.id,
            result_metadata = self.nlu_model.nlumodel_class.result_metadata,
        )
        orm_session.add(llm_obj)
        orm_session.commit()
        self.result_metadata = llm_obj

    @functools.cached_property
    def nlu_model(self) -> Union[NLUModelConfig, None]:
        """
        Get the selected model, use cached_property because this class initiate once every request
        """
        serving_model = filter_model_config(self.model_config, self.inference_request.nlu_model_name)
        if not serving_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='invalid model name',
            )
        return serving_model

    @property
    def result(self):
        res = {}
        LOG.info(f'inferencing')
        self.__insert_conversation()
        self.__insert_chat()
        self.nlu_model.nlumodel_class.predict_arg = self.inference_request.request_body
        self.nlu_model.nlumodel_class.preprocess()
        self.nlu_model.nlumodel_class.predict()
        self.nlu_model.nlumodel_class.postprocessing()
        self.__insert_llm_result()
        res['query'] = self.inference_request.request_body.get('query')
        res['result'] = self.nlu_model.nlumodel_class.prediction_result
        return res