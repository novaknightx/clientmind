import streamlit as st
from dotenv import load_dotenv
from clients import CLIENTS, seed_client_memories
from agent import get_opening_brief, chat_with_client
from memory import recall

load_dotenv()

# Page config
st.set_page_config(
    page_title="ClientMind",
    page_icon="🧠",
    layout="wide"
)

# Seed memories once per session
if "seeded" not in st.session_state:
    with st.spinner("Loading client memories..."):
        seed_client_memories()
    st.session_state.seeded = True

# --- SIDEBAR ---
st.sidebar.title("🧠 ClientMind")
st.sidebar.markdown("*Your clients. Never forgotten.*")
st.sidebar.divider()
st.sidebar.subheader("Select a Client")

selected_id = None
for client_id, data in CLIENTS.items():
    if st.sidebar.button(
        f"{data['avatar']} {data['name']}\n{data['project']}",
        key=client_id,
        use_container_width=True
    ):
        # Reset chat when switching clients
        if st.session_state.get("active_client") != client_id:
            st.session_state.active_client = client_id
            st.session_state.conversation = []
            st.session_state.brief = None

# --- MAIN AREA ---
if "active_client" not in st.session_state:
    st.title("Welcome to ClientMind 🧠")
    st.markdown("### Select a client from the sidebar to begin.")
    st.info("ClientMind remembers everything about your clients — feedback, preferences, deadlines, and history — so you never have to start from scratch.")
    st.stop()

client_id = st.session_state.active_client
client_data = CLIENTS[client_id]

# Two columns: chat + memory panel
col1, col2 = st.columns([2, 1])

with col1:
    st.title(f"{client_data['avatar']} {client_data['name']}")
    st.caption(f"Project: {client_data['project']}")
    
    # Generate opening brief once per client selection
    if not st.session_state.get("brief"):
        with st.spinner("Recalling client history..."):
            brief = get_opening_brief(
                client_id,
                client_data["name"],
                client_data["project"]
            )
        st.session_state.brief = brief
    
    # Show the memory-powered brief
    st.info(f"🧠 **Memory Brief:** {st.session_state.brief}")
    st.divider()
    
    # Chat history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        
        # Get and show agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_with_client(
                    client_id,
                    client_data["name"],
                    client_data["project"],
                    st.session_state.conversation[:-1],
                    user_input
                )
            st.write(reply)
        st.session_state.conversation.append({"role": "assistant", "content": reply})

with col2:
    st.subheader("🧠 Memory Panel")
    st.caption("What Hindsight remembers about this client")
    
    # Show stored memories
    memories = recall(client_id, "all preferences feedback deadlines communication")
    results = memories.get("results", [])
    
    if results:
        for i, mem in enumerate(results[:6]):
            content = mem.get("content", "")
            if content:
                st.markdown(f"""
                <div style='background:#1e1e2e;padding:10px;border-radius:8px;
                margin-bottom:8px;border-left:3px solid #7c3aed;font-size:13px;'>
                💾 {content[:120]}{'...' if len(content) > 120 else ''}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.caption("No memories yet. Start a conversation.")
    
    st.divider()
    st.caption(f"📊 {len(results)} memories stored for this client")