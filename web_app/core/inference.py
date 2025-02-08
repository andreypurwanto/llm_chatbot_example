# from web_app.models.inference import InferenceRequest
# from web_app.utils.helper import filter_model_config
# from web_app.base.model_loader import ModelLoader
# from web_app.models.nlu import NLUModelConfig
# from typing import Union
# from web_app.logs import LOG
# from fastapi import HTTPException, status
# from web_app.base.loader import model_configs

# def get_active_model_configs():
#     res = []
#     for model in model_configs.models:
#         temp_ = model.model_dump().copy()
#         if 'nlumodel_class' in temp_:
#             del temp_['nlumodel_class']  
#         res.append(temp_)
#     return res

# class Inference:
#     def __init__(self, inference_request: InferenceRequest, model_configs=model_configs):
#         self.inference_request = inference_request
#         self.model_config = model_configs
    
#     @property
#     def nlu_model(self) -> Union[NLUModelConfig, None]:
#         serving_model = filter_model_config(self.model_config, self.inference_request.nlu_model_name)
#         if not serving_model:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail='invalid model name',
#             )
#         return serving_model

#     @property
#     def result(self):
#         LOG.info(f'inferencing')
#         self.nlu_model.nlumodel_class.predict_arg = self.inference_request.request_body
#         self.nlu_model.nlumodel_class.preprocess()
#         self.nlu_model.nlumodel_class.predict()
#         return self.nlu_model.nlumodel_class.prediction_result