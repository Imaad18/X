import streamlit as st
import requests
import json
import time
import datetime
from typing import Optional, Dict, List
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64
import io

# Set page config with enhanced settings
st.set_page_config(
    page_title="🚀 AI Neural Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_css():
    """Inject custom futuristic CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(90deg, #00d4ff 0%, #7c3aed 50%, #f59e0b 100%);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
        margin: 0;
        letter-spacing: 3px;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #00d4ff;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(0, 212, 255, 0.2) 100%);
        border-color: #7c3aed;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(245, 158, 11, 0.2) 100%);
        border-color: #00d4ff;
    }
    
    /* Input field */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #00d4ff;
        border-radius: 10px;
        color: white;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.5);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #00d4ff;
        border-radius: 10px;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Stats panel */
    .stats-panel {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(26, 26, 46, 0.8) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid #00d4ff;
        margin: 1rem 0;
        backdrop-filter: blur(15px);
    }
    
    /* Custom text colors */
    .cyber-text {
        color: #00d4ff;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .warning-text {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .success-text {
        color: #10b981;
        font-weight: 600;
    }
    
    /* Animated loading */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 212, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00d4ff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Glassmorphism effect */
    .glass-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 10px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00d4ff;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_stats" not in st.session_state:
        st.session_state.chat_stats = {
            "total_messages": 0,
            "total_tokens": 0,
            "session_start": datetime.datetime.now(),
            "models_used": set(),
            "average_response_time": 0,
            "response_times": []
        }
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    if "current_session" not in st.session_state:
        st.session_state.current_session = "default"
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "cyber"

def get_model_info():
    """Extended model information with pricing and capabilities"""
    return {
        "Llama 3 70B": {
            "id": "llama3-70b-8192",
            "description": "Meta's most capable Llama 3 model",
            "context": "8K tokens",
            "price": "Free",
            "category": "Premium"
        },
        "Llama 3 8B": {
            "id": "llama3-8b-8192",
            "description": "Fast and efficient Llama 3 model",
            "context": "8K tokens",
            "price": "Free",
            "category": "Standard"
        },
        "Mixtral 8x7B": {
            "id": "mixtral-8x7b-32768",
            "description": "High-quality mixture of experts model",
            "context": "32K tokens",
            "price": "Free",
            "category": "Premium"
        },
        "Gemma 7B": {
            "id": "gemma-7b-it",
            "description": "Google's lightweight model",
            "context": "8K tokens",
            "price": "Free",
            "category": "Economy"
        }
    }

def estimate_tokens(text: str) -> int:
    """Rough token estimation"""
    return len(text.split()) * 1.3

def get_groq_response(messages, model="llama3-70b-8192", temperature=0.7, max_tokens=1000):
    """Enhanced API call with better error handling and stats tracking"""
    start_time = time.time()
    
    try:
        if "api_key" not in st.session_state or not st.session_state.api_key:
            st.error("🔐 **Neural Link Disconnected** - Please establish API connection in the sidebar.")
            return None
            
        api_key = st.session_state.api_key
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Update stats
            st.session_state.chat_stats["response_times"].append(response_time)
            st.session_state.chat_stats["average_response_time"] = sum(st.session_state.chat_stats["response_times"]) / len(st.session_state.chat_stats["response_times"])
            st.session_state.chat_stats["models_used"].add(model)
            
            if "usage" in result:
                st.session_state.chat_stats["total_tokens"] += result["usage"].get("total_tokens", 0)
            
            return content
        else:
            error_msg = f"🔴 **Neural Network Error {response.status_code}**"
            try:
                error_detail = response.json().get("error", {}).get("message", response.text)
                st.error(f"{error_msg}\n```{error_detail}```")
            except:
                st.error(f"{error_msg}\n```{response.text}```")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏱️ **Connection Timeout** - The AI is taking too long to respond. Try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 **Network Disruption**: {str(e)}")
        return None
    except Exception as e:
        st.error(f"⚠️ **System Anomaly**: {str(e)}")
        return None

def create_stats_dashboard():
    """Create an interactive stats dashboard"""
    stats = st.session_state.chat_stats
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 class="cyber-text">💬 Messages</h3>
            <h2 style="color: white; margin: 0;">{}</h2>
        </div>
        """.format(stats["total_messages"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 class="cyber-text">🔥 Tokens</h3>
            <h2 style="color: white; margin: 0;">{:,}</h2>
        </div>
        """.format(stats["total_tokens"]), unsafe_allow_html=True)
    
    with col3:
        avg_time = stats["average_response_time"]
        st.markdown("""
        <div class="metric-card">
            <h3 class="cyber-text">⚡ Avg Speed</h3>
            <h2 style="color: white; margin: 0;">{:.1f}s</h2>
        </div>
        """.format(avg_time), unsafe_allow_html=True)
    
    with col4:
        session_time = datetime.datetime.now() - stats["session_start"]
        st.markdown("""
        <div class="metric-card">
            <h3 class="cyber-text">🕐 Session</h3>
            <h2 style="color: white; margin: 0;">{}</h2>
        </div>
        """.format(str(session_time).split('.')[0]), unsafe_allow_html=True)

def export_chat_history():
    """Export chat history as JSON or text"""
    if not st.session_state.messages:
        st.warning("No chat history to export!")
        return
    
    # Create export data
    export_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "stats": dict(st.session_state.chat_stats),
        "messages": st.session_state.messages
    }
    
    # Convert set to list for JSON serialization
    export_data["stats"]["models_used"] = list(export_data["stats"]["models_used"])
    export_data["stats"]["session_start"] = export_data["stats"]["session_start"].isoformat()
    
    json_str = json.dumps(export_data, indent=2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Create readable text format
        text_export = f"AI Neural Interface Chat Export\n{'='*50}\n\n"
        for msg in st.session_state.messages:
            role = "🤖 AI" if msg["role"] == "assistant" else "👤 You"
            text_export += f"{role}:\n{msg['content']}\n\n"
        
        st.download_button(
            label="📄 Download Text",
            data=text_export,
            file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

def main():
    # Inject custom CSS
    inject_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Custom header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI NEURAL INTERFACE</h1>
        <p>Advanced Multi-Model AI Communication Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get model information
    model_info = get_model_info()
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown('<h2 class="cyber-text">🔧 CONTROL PANEL</h2>', unsafe_allow_html=True)
        
        # API Configuration
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("#### 🔑 Neural Link Authentication")
        
        api_key_input = st.text_input(
            "Groq API Key:",
            type="password",
            placeholder="gsk_...",
            help="Your Groq API key for neural network access"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.markdown('<p class="success-text">✅ Neural link established!</p>', unsafe_allow_html=True)
        elif "api_key" not in st.session_state:
            st.markdown('<p class="warning-text">⚠️ Neural link required</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model Configuration
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("#### 🧠 AI Model Selection")
        
        selected_model = st.selectbox(
            "Choose AI Model:",
            options=list(model_info.keys()),
            index=0,
            help="Select the AI model for processing"
        )
        
        # Display model info
        model_data = model_info[selected_model]
        st.markdown(f"""
        **{model_data['description']}**
        
        📊 **Context**: {model_data['context']}  
        💰 **Price**: {model_data['price']}  
        🏷️ **Category**: {model_data['category']}
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced Parameters
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("#### ⚙️ Neural Parameters")
        
        temperature = st.slider(
            "🌡️ Creativity Temperature:",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls AI creativity and randomness"
        )
        
        max_tokens = st.slider(
            "📏 Response Length:",
            min_value=100,
            max_value=8000,
            value=1500,
            step=100,
            help="Maximum response length in tokens"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Session Management
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("#### 💾 Session Control")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat_stats["total_messages"] = 0
                st.rerun()
        
        with col2:
            if st.button("📊 Reset Stats", use_container_width=True):
                st.session_state.chat_stats = {
                    "total_messages": 0,
                    "total_tokens": 0,
                    "session_start": datetime.datetime.now(),
                    "models_used": set(),
                    "average_response_time": 0,
                    "response_times": []
                }
                st.rerun()
        
        # Export options
        if st.session_state.messages:
            st.markdown("#### 📤 Export Data")
            export_chat_history()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    # Stats dashboard
    st.markdown('<div class="stats-panel">', unsafe_allow_html=True)
    st.markdown('<h3 class="cyber-text">📈 NEURAL NETWORK STATUS</h3>', unsafe_allow_html=True)
    create_stats_dashboard()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        # Display chat history with enhanced styling
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Add timestamp for recent messages
                if i >= len(st.session_state.messages) - 5:
                    st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Enhanced chat input
    if prompt := st.chat_input("🎯 Initialize neural communication..."):
        # Validate API key
        if "api_key" not in st.session_state or not st.session_state.api_key:
            st.error("🔐 **Neural Link Required** - Please establish API connection in the control panel.")
            st.stop()
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_stats["total_messages"] += 1
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Generate AI response
        with st.chat_message("assistant"):
            # Typing indicator
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div class="typing-indicator">
                <span>🤖 AI is processing</span>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Prepare API messages
            api_messages = st.session_state.messages[-30:]  # Keep last 30 messages
            
            response = get_groq_response(
                api_messages,
                model_info[selected_model]["id"],
                temperature,
                max_tokens
            )
            
            typing_placeholder.empty()
            
            if response:
                st.markdown(response)
                st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')} | Model: {selected_model}")
                
                # Add to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.chat_stats["total_messages"] += 1
                
                # Estimate tokens
                total_tokens = estimate_tokens(prompt + response)
                st.session_state.chat_stats["total_tokens"] += total_tokens
                
            else:
                st.error("🔴 **Neural communication failed** - Please retry or check your connection.")
    
    # Footer with enhanced info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #00d4ff; font-family: Orbitron, monospace;'>
        <h4>🚀 AI Neural Interface v2.0</h4>
        <p style='color: rgba(255,255,255,0.7);'>
            Powered by Groq API • Enhanced Neural Architecture • Built with Streamlit
        </p>
        <p style='color: rgba(0,212,255,0.8); font-size: 0.9rem;'>
            🔬 Advanced AI Communication Platform • 🌐 Multi-Model Support • 📊 Real-time Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
