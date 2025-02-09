import streamlit as st
import uuid
from web_app.logs import LOG
from streamlit_app.web_api import WebAPI

web_api = WebAPI()

def main_st():
    st.title("Testing LLM Chatbot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model_locked" not in st.session_state:
        st.session_state.model_locked = False
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = ""
    if "chat_ended" not in st.session_state:
        st.session_state.chat_ended = False
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    if "models" not in st.session_state:
        st.session_state.models = web_api.fetch_models()
    
    if not st.session_state.model_locked:
        st.session_state.selected_model = st.selectbox("Select LLM Model", st.session_state.models, key="model_selection") if st.session_state.models else None
    else:
        st.selectbox("Select LLM Model", st.session_state.models, index=st.session_state.models.index(st.session_state.selected_model), disabled=True) if st.session_state.models else None
    
    if not st.session_state.chat_ended:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        user_input = st.chat_input("Type your message...")
        
        if user_input:
            st.session_state.model_locked = True
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            
            if st.session_state.selected_model:
                bot_response = web_api.fetch_prediction(st.session_state.selected_model, user_input, st.session_state.conversation_id)
            else:
                bot_response = "No model selected."
            
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.chat_message("assistant").write(bot_response)
            LOG.info(f'USER chat {user_input} {st.session_state.conversation_id}')
        
        if st.button("End Chat"):
            st.session_state.chat_ended = True
            st.rerun()
    
    if st.session_state.chat_ended:
        st.write("### Please rate your experience")
        rating = st.radio("Did you like the chat?", ["Like", "Dislike"], key="rating")
        feedback = st.text_area("Optional feedback", key="feedback")
        
        if st.button("Start New Session"):
            web_api.send_review(rating, feedback, st.session_state.conversation_id)
            st.session_state.messages = []
            st.session_state.model_locked = False
            st.session_state.chat_ended = False
            LOG.info(f'end chat with rating {rating} {feedback} {st.session_state.conversation_id}')
            st.session_state.conversation_id = str(uuid.uuid4())
            st.session_state.models = web_api.fetch_models()
            st.rerun()
