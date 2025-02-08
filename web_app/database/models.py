from sqlalchemy import (
    Column, Integer, String, Boolean, JSON, Text, Date, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import VARCHAR
import uuid

Base = declarative_base()

# Models Table
class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # Changed to NOT NULL
    class_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)  # Changed to NULLABLE
    is_active = Column(Boolean, nullable=False)
    model_arg = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    conversations = relationship("Conversation", back_populates="model")
    llm_responses = relationship("LLMResponse", back_populates="model")
    chats = relationship("Chat", back_populates="model")


# Conversations Table
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    user_id = Column(VARCHAR(36), default=lambda: str(uuid.uuid4()), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    model = relationship("Model", back_populates="conversations")
    chats = relationship("Chat", back_populates="conversation")
    user_reviews = relationship("UserReview", back_populates="conversation")


# LLM Responses Table
class LLMResponse(Base):
    __tablename__ = "llm_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    llm_model_description = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    model = relationship("Model", back_populates="llm_responses")
    chats = relationship("Chat", back_populates="llm_response")


# Chats Table
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    llm_response_id = Column(Integer, ForeignKey("llm_responses.id"), nullable=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    query = Column(Text, nullable=True)
    remark = Column(JSON, default=None)  # JSON defaulting to NULL

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    conversation = relationship("Conversation", back_populates="chats")
    llm_response = relationship("LLMResponse", back_populates="chats")
    model = relationship("Model", back_populates="chats")


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