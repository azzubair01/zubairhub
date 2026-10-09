import os
from PIL import Image
import streamlit as st
from io import BytesIO
from tempfile import NamedTemporaryFile

from modules.utils.text_recognition import OCRExtractor

@st.cache_resource
def get_object_detector():
    from modules.utils.object_detection import DetrObjectDetection
    return DetrObjectDetection()

def detect_object():
    st.title("Let's detect objects 📷")
    option = st.radio(label='Select image option:', options=('Example', 'Upload'), key='Radio button for object detection option', horizontal=True)
    if option == 'Upload':
        # Streamlit file uploader for image input
        uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'jpeg', 'png'])
    elif option=='Example':
        example_image_list = os.listdir('modules/od_data')
        selected_image = st.selectbox(label='Select Example image', options=example_image_list)
        uploaded_file = f'modules/od_data/{selected_image}'

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
            detector = get_object_detector()
            labeled_image, detections = detector.detect_objects(img)

        # Provide download options if detections are successful
        if labeled_image and detections:

            # Create image buffer for download
            buf = BytesIO()
            labeled_image.save(buf, format="PNG")  # Save the labeled image into the buffer
            byte_im = buf.getvalue()  # Get byte od_data from buffer

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


def extract_text():
    st.title("Let's extract text 🔍")

    text = None
    uploaded_file = None

    col1, col2, col3 = st.columns(3)
    with col1:
        image_option = st.radio(label='Select image option:', options=('Example', 'Upload'), key='Radio button for image option', horizontal=True)

    if image_option == 'Upload':
        uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'jpeg', 'png'])

    elif image_option == 'Example':
        example_image_list = os.listdir('modules/ocr_data')
        selected_image = st.selectbox(label='Select Example image', options=example_image_list, key='Selectbox for image option')
        uploaded_file = f'modules/ocr_data/{selected_image}'


    with col2:
        config_option_list = [
            'Auto segmentation + OSD',
            'Auto segmentation + OCR',
            'Single Column Multi-size Text',
            'Vertical Text',
            'Text Block',
            'Single Line',
            'Single Word',
            'Single Word in Circle',
            'Single Character',
            'Sparse Text',
            'Sparse Text + OSD',
            'Raw Line'
        ]
        config_option = st.selectbox(label='Select OCR config', options=config_option_list)


    with col3:
        lang_list = ['eng', 'equ', 'msa', 'ara']
        selected_lang = st.multiselect(label='Select Language', default='eng', options=lang_list, key='Selectbox for language option')
        selected_lang = '+'.join(selected_lang) if selected_lang else ''

    ocr = OCRExtractor(lang=selected_lang)
    temp_file_path = None

    try:
        text = None
        img = None

        if image_option == 'Upload':
            if uploaded_file is None:
                st.error("No file uploaded yet.")
            else:
                suffix = os.path.splitext(uploaded_file.name)[1]
                temp_file = NamedTemporaryFile(delete=False, suffix=suffix)
                temp_file.write(uploaded_file.getbuffer())
                temp_file.close()
                temp_file_path = temp_file.name

                with st.spinner("Running OCR..."):
                    text = ocr.extract_text(temp_file_path, config_option)
                img = Image.open(temp_file_path).copy()

        elif image_option == 'Example':
            if uploaded_file is not None and os.path.exists(uploaded_file):
                with st.spinner("Running OCR..."):
                    text = ocr.extract_text(uploaded_file, config_option)
                img = Image.open(uploaded_file)

        if img is not None:
            with st.expander(label='Preview image:', expanded=True):
                st.image(img)
            if text:
                st.info(f"Detected text: \n\n{text}")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass

