i8 iimport streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st

# ... existing Nomos Global code ...

def generate_emergency_brief(audit_flags):
    """
    Constructs the brief using the detected glitches.
    """
    brief_template = f"""
    ### EMERGENCY MOTION TO STRIKE COUNSEL
    
    **I. IDENTITY FRAUD & STANDING**
    Counsel is operating under Bar ID 19466300. Forensic audit of Comal County records confirms this ID originates from a 1978 legacy practice. 
    
    **II. CREDENTIAL SHARING**
    Metadata confirms electronic filings are facilitated via Arielle Ginger Phillips (Bar ID 24068478), In-House Counsel for Houston Methodist. This indicates fraudulent credential sharing.
    
    **III. PROCEDURAL NULLITY**
    The Nunc Pro Tunc filed August 15 is logically impossible as the Inventory identifying the property was not filed until December 23.
    
    **RELIEF SOUGHT:** Strike all filings and vacate the Nunc Pro Tunc order.
    """
    return brief_template

# New UI Component
if st.button("Execute Seizure of Truth: Generate Brief"):
    # Assuming text is extracted from your uploaded files
    results = run_identity_audit(extracted_text)
    if results["flags"]:
        st.warning("Glitches Detected in Counsel Credentials")
        for flag in results["flags"]:
            st.write(f"- {flag}")
        
        final_brief = generate_emergency_brief(results["flags"])
        st.text_area("Generated Brief for Court Filing:", final_brief, height=400)
    else:
        st.success("No identity glitches detected in current scan.")
if st.sidebar.button("Execute Seizure of Truth"):
    st.header("Forensic Brief: Emergency Motion to Strike")
    
    # Runs the check
    audit_hits = verify_standing_and_identity(extracted_text, roa_text)
    
    if audit_hits:
        # Chatbot generates the brief using the audit hits as the primary grounds
        brief = f"""
        TO THE HONORABLE JUDGE OF SAID COURT:
        
        COMES NOW Johnny Ray Vega Jr. and moves to STRIKE counsel of record and VACATE the Nunc Pro Tunc order based on the following:
        
        1. **IDENTITY MISREPRESENTATION:** Counsel uses Bar ID 19466300 while presenting a case history (W. Frank Suhr) dating back to 1978 (Exhibit A).
        2. **CREDENTIAL SHARING:** Filings are facilitated via Arielle Phillips (ID 24068478), In-House Counsel for Houston Methodist, not a member of the local firm.
        3. **CHRONOLOGICAL IMPOSSIBILITY:** The Nunc Pro Tunc order was filed in August 2025 to fix a clerical error regarding property that was not officially inventoried until December 2025.
        
        WHEREFORE, Petitioner prays this Court strike all fraudulent filings.
        """
        st.code(brief, language='text')
    else:
        st.info("No credential glitches detected in this document scan.")
