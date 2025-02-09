import json
from fastapi import Request, HTTPException, status, Depends
from web_app.models.api import ReviewRequest
from web_app.logs import LOG
from web_app.logs.log_tracer import set_get_trace_id
from web_app.base.auth import BasicAuth
from uuid import uuid4
from web_app.logs.log_tracer import set_get_trace_id

basic_auths = BasicAuth().get_all_basic_auth()

async def get_body(request: Request) -> bytes:
    return await request.body()

def get_review_request(request: Request, body: bytes = Depends(get_body)) -> ReviewRequest:
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
    
    mandatory_key = ['star', 'feedback']
    for key in mandatory_key:
        if key not in body:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'missing mandatory'
            )
    
    if not isinstance(body['star'], int):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'invalid type star'
            )
    
    if not isinstance(body['feedback'], str):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'invalid type feedback'
            )

    LOG.info(f'get_review_request {body}')

    return ReviewRequest(
        star=body['star'],
        feedback=body['feedback'],
        trace_id=trace_id,
        conversation_external_id=conv_ext_id
    )

def extract_request_review(review_request: ReviewRequest = Depends(get_review_request)):
    return review_request