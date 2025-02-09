from sqlalchemy import (
    Column, Integer, String, Boolean, JSON, Text, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import VARCHAR
import uuid

Base = declarative_base()

# Models Table
class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    class_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False)
    model_arg = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    conversations = relationship("Conversation", back_populates="model")


# Conversations Table
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    user_id = Column(VARCHAR(36), default=lambda: str(uuid.uuid4()), nullable=True)
    external_id = Column(Text, nullable=False)  # Newly added column
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    model = relationship("Model", back_populates="conversations")
    chats = relationship("Chat", back_populates="conversation")
    user_reviews = relationship("UserReview", back_populates="conversation")


# Chats Table
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    query = Column(Text, nullable=True)
    remark = Column(JSON, default=None)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    conversation = relationship("Conversation", back_populates="chats")
    llm_results = relationship("LLMResult", back_populates="chat")


# LLM Results Table
class LLMResult(Base):
    __tablename__ = "llm_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    result_metadata = Column(JSON, default=None)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    chat = relationship("Chat", back_populates="llm_results")


# User Reviews Table
class UserReview(Base):
    __tablename__ = "user_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    feedback = Column(Text, nullable=True)
    star = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    conversation = relationship("Conversation", back_populates="user_reviews")