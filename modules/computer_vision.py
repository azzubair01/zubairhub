import json
import os

from PIL import Image
import streamlit as st
from io import BytesIO
from modules.utils.object_detection import DetrObjectDetection

detector = DetrObjectDetection()

def detect_object():
    option = st.radio(label='Select image option:', options=('Example', 'Upload'), key='Radio button for object detection option', horizontal=True)
    if option == 'Upload':
        # Streamlit file uploader for image input
        uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'jpeg', 'png'])
    elif option=='Example':
        example_image_list = os.listdir('modules/data')
        selected_image = st.selectbox(label='Select Example image', options=example_image_list)
        uploaded_file = f'modules/data/{selected_image}'

    # Throw error if no file is uploaded
    if uploaded_file is None:
        st.error("No file uploaded yet.")
    else:
        try:
            # Load image from the uploaded file
            img = Image.open(uploaded_file)
            with st.expander(label='Preview image:', expanded=False):
                st.image(img)
        except Exception as e:
            st.error(f"Error opening image: {str(e)}")

        # Run object detection
        with st.spinner("Running object detection..."):
            labeled_image, detections = detector.detect_objects(img)

        # Provide download options if detections are successful
        if labeled_image and detections:

            # Create image buffer for download
            buf = BytesIO()
            labeled_image.save(buf, format="PNG")  # Save the labeled image into the buffer
            byte_im = buf.getvalue()  # Get byte data from buffer

            # Display the results and allow image download
            st.subheader("Object Detection Predictions")
            st.image(labeled_image)  # Display annotated image

            # Add a download button for the annotated image
            st.download_button(
                label='Download Image',
                data=byte_im,
                file_name="image_object_detection.png",
                mime="image/png",
                type='primary',
                use_container_width=True
            )
            # Display and allow download of predictions as JSON
            # st.json(detections)  # Display the detections as a JSON object

        else:
            # Handle case where no objects are detected
            st.warning("No objects detected.")
