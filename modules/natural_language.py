import os
import pandas as pd
import streamlit as st
from tempfile import NamedTemporaryFile
from streamlit_pdf_viewer import pdf_viewer
from modules.utils.document_parser import PDFExtractor


def parse_document():
    st.title("Let's parse documents 📄")

    # Select input option
    option = st.radio(
        label='Select input option:',
        options=('Example', 'Upload'),
        key='Radio button for parse document option',
        horizontal=True
    )

    uploaded_file = None
    file_path = None  # Path to the actual file
    is_temp = False

    col1, col2 = st.columns(2)

    with col1:
        if option == 'Upload':
            uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
            if uploaded_file is None:
                st.error("No file uploaded yet.")
            else:
                temp_file = NamedTemporaryFile(delete=False, suffix=".pdf")
                temp_file.write(uploaded_file.getbuffer())
                temp_file.close()
                file_path = temp_file.name
                is_temp = True
        elif option == 'Example':
            example_document_list = os.listdir('modules/nlp_data')
            selected_document = st.selectbox('Select Example PDF', example_document_list)
            file_path = f'modules/nlp_data/{selected_document}'

    if file_path:
        try:
            # Read PDF file as binary
            with open(file_path, "rb") as f:
                pdf_binary = f.read()

            # Initialize PDF extractor with context manager
            with PDFExtractor(file_path) as pdf_extractor:
                # Select page for extraction
                num_pages = pdf_extractor.total_pages
                range_pages = list(range(1, num_pages + 1))

                with col2:
                    page_num = st.selectbox("Select Page to Extract", options=range_pages, key='Selectbox for page option')

                col1, col2 = st.columns(2)

                with col1:
                    # Display PDF preview
                    pdf_viewer(input=pdf_binary, width=700, pages_to_render=[page_num], height=500)

                with col2:
                    # Extract text from selected page
                    extracted_text = pdf_extractor.extract_text(page_num)
                    st.text_area("Extracted Text:", extracted_text['extracted_text'], height=400)

                extracted_table = pdf_extractor.extract_tables(page_num)

                if not pd.DataFrame(extracted_table['extracted_text']).empty:
                    st.info(f'Table detected on page {page_num}')
                    st.dataframe(extracted_table['extracted_text'], use_container_width=True, hide_index=True)
                else:
                    st.warning(f'No table detected on page {page_num}')

        except Exception as e:
            st.error(f"Error opening document: {str(e)}")
        finally:
            if is_temp and file_path and os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except OSError:
                    pass
