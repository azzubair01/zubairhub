import streamlit as st
from PIL import Image
from modules.utils.generative_ai import generate_response


def generative_ai():
    """Streamlit interface for AI prompt generation with text and image."""
    st.title("Let's Chat with AI 🔮")
    st.write("Input text and optionally upload an image.")

    # Text Input
    user_text = st.text_area("Enter your prompt:", key='Text area for ai prompt', value="Describe this image.")

    # Image Input (Optional)
    uploaded_image = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg"])

    # Process Image
    image = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Submit Button
    if st.button("Generate Response"):
        if user_text.strip():
            with st.spinner("Generating response..."):
                response_text = generate_response(user_text, image)
                st.subheader("AI Response:")
                st.info(response_text)
        else:
            st.warning("Please enter a text prompt.")