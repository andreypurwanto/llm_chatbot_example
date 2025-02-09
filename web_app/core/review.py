from web_app.models.api import ReviewRequest
from web_app.utils.helper import filter_model_config
from web_app.base.model_loader import ModelLoader
from web_app.models.nlu import NLUModelConfig
from typing import Union
from web_app.logs import LOG
from fastapi import HTTPException, status
from web_app.base.loader import model_configs
from web_app.database import orm_session, UserReview, Conversation
import functools
from fastapi import HTTPException, status

class Review:
    def __init__(self, review_request: ReviewRequest):
        self.review_request = review_request
    
    @functools.cached_property
    def conversation(self) -> Union[Conversation, None]:
        conv = orm_session.query(Conversation).filter(Conversation.external_id == self.review_request.conversation_external_id)
        if conv: return conv.first()
        return conv
    
    @functools.cached_property
    def review(self) -> Union[UserReview, None]:
        if conv := self.conversation:
            rev = orm_session.query(UserReview).filter(UserReview.conversation_id == conv.id)
            if rev: return rev.first()
        return None
    
    def insert_review(self) -> None:
        if not self.conversation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='invalid conversation external id',
            )
        
        if self.review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='duplicate review',
            )
        
        rev = UserReview(
            conversation_id = self.conversation.id,
            feedback = self.review_request.feedback,
            star = self.review_request.star
        )
        orm_session.add(rev)
        orm_session.commit()
        return

