import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="WhatsApp AI Assistant",
    page_icon="💬",
    layout="centered"
)

# 2. Custom CSS for WhatsApp-like styling
st.markdown("""
<style>
    /* WhatsApp Dark Theme Canvas Background */
    .stApp {
        background-color: #0b141a;
    }
    
    /* Persona Header Card */
    .persona-card {
        background-color: #202c33;
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #e9edef;
        border-left: 5px solid #00a884;
    }
    
    /* WhatsApp Chat Input Tweaks */
    .stChatInputContainer {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_allow_html=True)

# 3. Sidebar Configuration
st.sidebar.title("💬 WhatsApp AI")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(
    "🔑 Groq API Key:",
    type="password",
    help="Get your free API key at console.groq.com"
)

# Persona Selection
personas = {
    "Helpful Assistant 🤖": "You are a friendly, concise WhatsApp AI assistant. Respond in clear, helpful sentences.",
    "Coding Expert 💻": "You are a pragmatic senior software developer. Give precise, clean code solutions with brief explanations.",
    "Creative Writer ✍️": "You are an imaginative storyteller. Write engaging, evocative responses.",
    "Fitness Coach 🏋️": "You are a high-energy fitness and nutrition coach. Give actionable, motivating advice."
}

selected_persona = st.sidebar.selectbox("Choose Persona:", list(personas.keys()))
system_prompt = personas[selected_persona]

# Clear Chat History Button
if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Powered by **Streamlit** & **Groq Llama 3.3**")

# 4. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Header Bar
st.markdown(f"""
<div class="persona-card">
    <h3 style="margin: 0; color: #00a884;">💬 {selected_persona}</h3>
    <p style="margin: 4px 0 0 0; font-size: 0.85rem; opacity: 0.8;">Online | Powered by Groq Llama 3.3</p>
</div>
""", unsafe_allow_html=True)

# 6. Display Chat History
for message in st.session_state.messages:
    # Use native Streamlit chat message containers for WhatsApp-style avatars and bubbles
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 7. Chat Input and Streaming Response
if prompt := st.chat_input("Type a message..."):
    # Validate API key
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to start chatting.")
    else:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            try:
                client = Groq(api_key=api_key)

                # Prepare payload with System Prompt + Chat History
                conversation_history = [{"role": "system", "content": system_prompt}] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]

                # Stream response word-by-word
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=conversation_history,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=True
                )

                # Collect response live
                full_response = st.write_stream(stream)

                # Append Assistant Response to State
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error: {str(e)}")