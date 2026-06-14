import streamlit as st
from PIL import Image
from modules.utils.generative_ai import generate_response


def generative_ai():
    """Streamlit interface for AI prompt generation with text and image."""
    st.title("Let's Chat with AI 🔮")
    st.write("Input text and optionally upload an image.")

    # RACE Inputs
    role = st.text_input("Role (Who is the AI supposed to be?):", value="An expert in AI", key='Text area for role')
    action = st.text_input("Action (What do you want it to do?):", value="Explain the concept of AI", key='Text area for action')
    context = st.text_area("Context (Provide any relevant background info):", value="The user is a beginner interested in learning about AI.", key='Text area for context')
    expectation = st.text_area("Expectation (What kind of output are you expecting?):", value="Give a clear and simple explanation with examples.", key='Text area for expectation')

    # Combine RACE into a prompt
    full_prompt = f"Role: {role}\nAction: {action}\nContext: {context}\nExpectation: {expectation}"

    # Show constructed prompt in an expander
    with st.expander("📝 View Constructed Prompt", expanded=False):
        st.code(full_prompt)

    with st.expander(label='Upload image', icon='🖼️'):
        # Image Input (Optional)
        uploaded_image = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg"])

    # Process Image
    image = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        with st.expander("🖼️ View Uploaded Image", expanded=True):
            st.image(image, caption="Uploaded Image", width="stretch")

    # Submit Button
    if st.button("Generate Response"):
        if full_prompt.strip():
            with st.spinner("Generating response..."):
                response_text = generate_response(
                    full_prompt, 
                    image, 
                    model_name=st.session_state.get('selected_model')
                )
                with st.expander("🔮 View AI Response", expanded=True):
                    st.info(response_text)
        else:
            st.warning("Please enter a text prompt.")