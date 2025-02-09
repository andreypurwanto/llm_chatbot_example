from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import (
    Model,
    Conversation,
    LLMResult,
    Chat,
    UserReview
)
from web_app.constant.database import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME

engine = create_engine(
    f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    echo=True,
    poolclass=NullPool,
    pool_recycle=60,
)

orm_session = scoped_session(sessionmaker(bind=engine))