"""
Streamlit frontend for Medical Document Assistant.
Provides a user interface for uploading documents and asking questions.
"""
import streamlit as st
import requests
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
DEFAULT_USERNAME = os.getenv("DEMO_USERNAME", "medical_researcher")
DEFAULT_PASSWORD = os.getenv("DEMO_PASSWORD", "demo_password_123")

# Page config
st.set_page_config(
    page_title="Medical Document Assistant",
    page_icon="🏥",
    layout="wide"
)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []


def login(username: str, password: str) -> bool:
    """Authenticate with the API."""
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            return True
        return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def upload_file(file) -> dict:
    """Upload a file to the API."""
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    files = {"file": (file.name, file, file.type)}
    
    try:
        response = requests.post(
            f"{API_URL}/upload",
            headers=headers,
            files=files
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        return None


def ask_question(question: str) -> dict:
    """Ask a question to the API."""
    headers = {
        "Authorization": f"Bearer {st.session_state.token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/ask",
            headers=headers,
            json={"question": question}
        )
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            st.error(f"Error: {error_detail}")
            return None
    except Exception as e:
        st.error(f"Error asking question: {e}")
        return None


def main():
    """Main application."""
    st.title("🏥 Medical Document Assistant")
    st.markdown("---")
    
    # Login section
    if not st.session_state.token:
        st.header("🔐 Login")
        st.info("Demo credentials are pre-filled. Click 'Login' to continue.")
        
        with st.form("login_form"):
            username = st.text_input("Username", value=DEFAULT_USERNAME)
            password = st.text_input("Password", type="password", value=DEFAULT_PASSWORD)
            submit = st.form_submit_button("Login")
            
            if submit:
                if login(username, password):
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        st.markdown("---")
        st.markdown("""
        ### About this Assistant
        
        This medical document assistant helps researchers:
        - 📄 Upload clinical and medical documents (PDF, TXT)
        - 💬 Ask questions about the documents
        - 🔍 Get answers with relevant context and sources
        
        **Features:**
        - Protected API with authentication
        - OpenAI-powered question answering
        - Context-aware responses with source citations
        - Basic observability and logging
        """)
        return
    
    # Main application (authenticated)
    st.sidebar.header("📁 Document Management")
    
    # File upload
    st.sidebar.subheader("Upload Documents")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a PDF or TXT file",
        type=['pdf', 'txt'],
        help="Upload medical or clinical documents for analysis"
    )
    
    if uploaded_file is not None:
        if st.sidebar.button("📤 Process Document"):
            with st.spinner("Processing document..."):
                result = upload_file(uploaded_file)
                if result:
                    st.sidebar.success(f"✅ {result['message']}")
                    st.sidebar.info(f"Created {result['chunks_created']} text chunks")
                    st.session_state.uploaded_files.append(result['filename'])
    
    # Show uploaded files
    if st.session_state.uploaded_files:
        st.sidebar.subheader("Uploaded Files")
        for filename in st.session_state.uploaded_files:
            st.sidebar.text(f"📄 {filename}")
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.session_state.messages = []
        st.session_state.uploaded_files = []
        st.rerun()
    
    # Main chat interface
    st.header("💬 Ask Questions")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {i}:** {source['source']} (Chunk {source['chunk']})")
                        st.caption(source['content'])
                        st.markdown("---")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_question(prompt)
                
                if response:
                    st.markdown(response["answer"])
                    
                    # Store message with sources
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response["sources"]
                    })
                    
                    # Show sources
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(response["sources"], 1):
                            st.markdown(f"**Source {i}:** {source['source']} (Chunk {source['chunk']})")
                            st.caption(source['content'])
                            st.markdown("---")
                else:
                    error_msg = "Sorry, I couldn't process your question. Please make sure you've uploaded documents first."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "sources": []
                    })
    
    # Instructions
    if not st.session_state.messages and not st.session_state.uploaded_files:
        st.info("""
        ### 👋 Welcome! Get started:
        
        1. **Upload a document** using the sidebar (PDF or TXT format)
        2. **Ask questions** about your documents in the chat
        3. **Review sources** to see where answers come from
        
        Example questions:
        - "What are the main findings of this study?"
        - "What medications are mentioned?"
        - "Summarize the patient outcomes"
        - "What are the side effects discussed?"
        """)


if __name__ == "__main__":
    main()
