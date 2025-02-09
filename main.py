import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
#then import 
import chromadb

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
# from web_app.utils.rate_limiter import rate_limit_healthcheck, rate_limit_search
from web_app.logs import LOG
from web_app.constant.common import ENV
from web_app.models import HealtcheckResponse
from web_app.core import Inference, get_active_model_configs, Review
from web_app.models.api import InferenceRequest, ReviewRequest
from web_app.api.dependencies import extract_request_inference, extract_request_review
from fastapi import HTTPException, status

app = FastAPI()

@app.post('/v1/model/{model_name}/prediction_result')
def get_prediction_result(inference_request: Annotated[InferenceRequest, Depends(extract_request_inference)]):
    try:
        inference = Inference(inference_request)
        result = inference.result
        result = {
            'success': True,
            'data': result 
        }
        status_code = 200
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        LOG.error(f'error api predict inference {inference_request.model_dump()} {e}', exc_info=True)
        result = {
            'success': False,
            'status': 'ERROR'
        }
        status_code = 500
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )

@app.post('/v1/review')
def user_review(review_request: Annotated[ReviewRequest, Depends(extract_request_review)]):
    try:
        review = Review(review_request)
        review.insert_review()
        result = {
            'success': True
        }
        status_code = 200
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        LOG.error(f'error user review{e}', exc_info=True)
        result = {
            'success': False,
            'status': 'ERROR'
        }
        status_code = 500
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )
        

@app.get('/v1/model/{model_name}')
def get_model_config(inference_request: Annotated[InferenceRequest, Depends(extract_request_inference)]):
    try:
        inference = Inference(inference_request)
        result = inference.nlu_model.model_dump().copy()
        if 'nlumodel_class' in result:
            del result['nlumodel_class']  
        result = {
            'success': True,
            'data': result 
        }
        status_code = 200
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        LOG.error(f'error api predict inference {inference_request.model_dump()} {e}', exc_info=True)
        result = {
            'success': False,
            'status': 'ERROR'
        }
        status_code = 500
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )

@app.get('/v1/model')
def get_model_config():
    try:
        result = get_active_model_configs()
        result = {
            'success': True,
            'data': result 
        }
        status_code = 200
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        result = {
            'success': False,
            'status': 'ERROR'
        }
        status_code = 500
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(result),
        )

@app.get('/healthcheck')
def healthcheck():
    LOG.debug(f'run main inference healthcheck from env: {ENV}')
    resp = HealtcheckResponse(
        status='ok',
        environment=ENV
    )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(resp)
    )