from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from fastapi import Request, HTTPException, status, Depends
from web_app.utils import get_config_value
from web_app.logs import LOG
from web_app.base import BaseNLUModel
from web_app.constant.openai import OPENAI_API_KEY

# Default system template for processing customer queries
REVIEW_SYSTEM_TEMPATE_STR = """
    Your job is to answer question from customer of LinkAJA. 
    Use the following context to answer questions.
    Be as detailed as possible, but don't make up any information
    that's not from the context. If you don't know an answer, say
    you don't know and say that you only answer LinkAja related question. 
    Answer in Bahasa Indonesia if question in Bahasa Indonesia, else answer in English.

    {context}
"""

class OpenAIRAG(BaseNLUModel):
    def __init__(self, args):
        LOG.info(f'Initializing OpenAIRAG')
        
        # Ensure required arguments are provided
        if not args.get('chroma_path'):
            raise Exception('Invalid argument: chroma_path is required')
        
        if not args.get('model_args'):
            raise Exception('Invalid argument: model_args is required')
        
        self.args = args
        self.chat_model = ChatOpenAI(**args.get('model_args'), openai_api_key=OPENAI_API_KEY)
        self.review_chain = None
        self._predict_arg = None
        self._prediction_result = None
        self._result_metadata = None
        self.build_chain()

    def build_chain(self):
        """
        Builds the RAG chain
        """
        LOG.info(f'Building chain for OpenAIRAG')
        
        # Load the vector database for retrieval
        reviews_vector_db = Chroma(
            persist_directory=self.args.get('chroma_path'),
            embedding_function=OpenAIEmbeddings()
        )

        # Use a custom review system template if provided, otherwise use default
        review_system_template_str = self.args.get('review_system_template_str', REVIEW_SYSTEM_TEMPATE_STR)
        
        if not review_system_template_str:
            raise Exception('Missing review_system_template_str')

        # Create prompt templates for system and user input
        review_system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"], template=review_system_template_str
            )
        )

        review_human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["question"], template="{question}"
            )
        )

        # Define the chat prompt template combining system and user prompts
        messages = [review_system_prompt, review_human_prompt]
        review_prompt_template = ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=messages,
        )

        # Retrieve relevant context from the vector database
        reviews_retriever = reviews_vector_db.as_retriever(k=10)

        # Define the final processing chain
        review_chain = (
            {"context": reviews_retriever, "question": RunnablePassthrough()}
            | review_prompt_template
            | self.chat_model
        )

        self.review_chain = review_chain
    
    @property
    def predict_arg(self):
        return self._predict_arg
    
    @predict_arg.setter
    def predict_arg(self, val):
        """
        Validates and sets the input query for prediction
        """
        if not val.get('query'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Missing required query parameter'
            )
        self._predict_arg = val
    
    def preprocess(self):
        """
        Preprocesses input query by converting it to lowercase
        """
        self.predict_arg['query'] = self.predict_arg.get('query').lower()

    def postprocessing(self):
        # placeholder
        pass

    @property
    def prediction_result(self):
        return self._prediction_result
    
    @property
    def result_metadata(self):
        return self._result_metadata
    
    def predict(self):
        """
        Runs the prediction process using the RAG pipeline
        """
        res = self.review_chain.invoke(self.predict_arg.get('query'))
        self._prediction_result = res.content
        self._result_metadata = res.response_metadata