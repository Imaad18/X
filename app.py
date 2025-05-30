import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="OpenRouter Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_openrouter_response(messages, model="openai/gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
    """Send request to OpenRouter API and get response"""
    try:
        # Get API key from session state
        if "api_key" not in st.session_state or not st.session_state.api_key:
            st.error("❌ Please enter your API key in the sidebar first.")
            return None
            
        api_key = st.session_state.api_key
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",  # Optional: your app's URL
            "X-Title": "Streamlit Chatbot"  # Optional: your app's name
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

# App header
st.title("🤖 OpenRouter Chatbot")
st.markdown("Chat with AI models through OpenRouter API")

# Sidebar for API key and settings
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # API Key input
    api_key_input = st.text_input(
        "Enter OpenRouter API Key:",
        type="password",
        placeholder="sk-or-v1-...",
        help="Enter your OpenRouter API key"
    )
    
    # Store API key in session state
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ API Key entered successfully!")
    elif "api_key" not in st.session_state:
        st.warning("⚠️ Please enter your API key to start chatting")
    
    st.markdown("---")
    st.header("⚙️ Model Settings")
    
    # Model selection
    model_options = {
        "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
        "GPT-4": "openai/gpt-4",
        "Claude 3 Haiku": "anthropic/claude-3-haiku",
        "Claude 3 Sonnet": "anthropic/claude-3-sonnet",
        "Llama 2 70B": "meta-llama/llama-2-70b-chat",
        "Mistral 7B": "mistralai/mistral-7b-instruct"
    }
    
    selected_model = st.selectbox(
        "Choose Model:",
        options=list(model_options.keys()),
        index=0
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature:",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness. Lower = more focused, Higher = more creative"
    )
    
    # Max tokens slider
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
        help="Maximum length of the response"
    )
    
    st.markdown("---")
    st.header("🗑️ Chat Management")
    
    # Clear chat button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Display current settings
    st.markdown("---")
    st.header("📊 Current Settings")
    st.info(f"**Model:** {selected_model}")
    st.info(f"**Temperature:** {temperature}")
    st.info(f"**Max Tokens:** {max_tokens}")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Check if API key is provided
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.error("⚠️ Please enter your OpenRouter API key in the sidebar first!")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare messages for API (limit to last 10 exchanges to manage token usage)
            api_messages = st.session_state.messages[-20:]  # Keep last 20 messages
            
            response = get_openrouter_response(
                api_messages, 
                model_options[selected_model],
                temperature,
                max_tokens
            )
            
            if response:
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("Failed to get response from the API. Please try again.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Powered by OpenRouter API | Built with Streamlit</small>
    </div>
    """, 
    unsafe_allow_html=True
)
