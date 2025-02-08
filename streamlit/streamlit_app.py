import streamlit as st
import uuid
from web_app.logs import LOG

def main():
    st.title("Echo Chatbot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model_locked" not in st.session_state:
        st.session_state.model_locked = False
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "ChatGPT"
    if "chat_ended" not in st.session_state:
        st.session_state.chat_ended = False
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())  # Initialize conversation_id on first run
    
    if not st.session_state.model_locked:
        st.session_state.selected_model = st.selectbox("Select LLM Model", ["ChatGPT", "Llama"], key="model_selection")
    else:
        st.selectbox("Select LLM Model", ["ChatGPT", "Llama"], index=["ChatGPT", "Llama"].index(st.session_state.selected_model), disabled=True)
    
    if not st.session_state.chat_ended:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        user_input = st.chat_input("Type your message...")
        
        if user_input:
            st.session_state.model_locked = True
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            
            bot_response = user_input  # Echo the user input
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.chat_message("assistant").write(bot_response)
            LOG.info(f'AAAA chat {user_input} {st.session_state.conversation_id}')
        
        if st.button("End Chat"):
            st.session_state.chat_ended = True
            st.rerun()
    
    if st.session_state.chat_ended:
        st.write("### Please rate your experience")
        rating = st.radio("Did you like the chat?", ["Like", "Dislike"], key="rating")
        feedback = st.text_area("Optional feedback", key="feedback")
        
        if st.button("Start New Session"):
            st.session_state.messages = []
            st.session_state.model_locked = False
            st.session_state.chat_ended = False
            LOG.info(f'end chat with rating {rating} {feedback} {st.session_state.conversation_id}')
            st.session_state.conversation_id = str(uuid.uuid4())  # Change conversation_id on new session
            st.rerun()

if __name__ == "__main__":
    main()