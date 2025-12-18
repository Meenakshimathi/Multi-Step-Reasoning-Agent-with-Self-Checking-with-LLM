import streamlit as st
from agent import ReasoningAgent

st.set_page_config(page_title="Reasoning Agent", layout="wide")
st.title("🧠 Multi-Step Reasoning Agent")

if "agent" not in st.session_state:
    st.session_state.agent = ReasoningAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "data" in msg:
            with st.expander("Debug Metadata"):
                st.json(msg["data"])

# User input
prompt = st.chat_input("Ask a math or logic question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Agent is working...", expanded=True) as status_box:

            def stream_update(step, text):
                status_box.write(f"**{step}**")
                status_box.markdown(text)

            response = st.session_state.agent.solve(prompt, callback=stream_update)

        final_text = f"""
### ✅ Answer
**{response["answer"]}**

**Explanation:**  
{response["reasoning_visible_to_user"]}
"""
        st.markdown(final_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": final_text,
        "data": response
    })
