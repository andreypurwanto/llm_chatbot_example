import json
from fastapi import Request, HTTPException, status, Depends
from web_app.models.api import InferenceRequest
from web_app.logs import LOG
from web_app.logs.log_tracer import set_get_trace_id
from web_app.base.auth import BasicAuth
from uuid import uuid4
from web_app.logs.log_tracer import set_get_trace_id

basic_auths = BasicAuth().get_all_basic_auth()

async def get_body(request: Request) -> bytes:
    return await request.body()

def get_inference_request(model_name, request: Request, body: bytes = Depends(get_body)) -> InferenceRequest:
    body = json.loads(body.decode('utf-8')) if body else {}
    conv_ext_id = body.get('conv_ext_id',str(uuid4()))
    trace_id = set_get_trace_id(body.get('trace_id',conv_ext_id))

    auth_ = request.headers.get('Authorization')
    if not auth_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header is mandatory',
        )

    if (not (auth_ in basic_auths)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Authorization',
        )

    LOG.info(f'get_inference_request {body}')

    return InferenceRequest(
        nlu_model_name=model_name,
        request_body=body,
        trace_id=trace_id,
        conversation_external_id=conv_ext_id
    )

def extract_request_inference(inference_request: InferenceRequest = Depends(get_inference_request)):
    return inference_request