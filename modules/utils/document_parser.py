import os
import logging
import pymupdf
import pandas as pd
import streamlit as st

# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PDFExtractor:
    def __init__(self, file_path):
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path
        self.doc = None
        self.pdf_data = []
        self.df = None
        self.total_pages = 0
        self.open_pdf()

    def open_pdf(self):
        self.doc = pymupdf.open(self.file_path)
        self.logger.info(f'Reading {self.file_path} with {len(self.doc)} pages')
        self.total_pages = len(self.doc)

    def extract_text(self, page_no:int):
        if not self.doc:
            raise ValueError("PDF document is not opened.")
        page_no = page_no - 1
        if page_no < 0 or page_no >= self.total_pages:
            raise ValueError("Invalid page number.")

        extracted_dict = {
            'page_no': page_no,
            'extracted_text': None,
            'type': 'text_extraction'
        }
        page = self.doc[page_no]
        text = page.get_text()
        if text:
            extracted_dict['extracted_text'] = text
            self.pdf_data.append(extracted_dict)
        return extracted_dict

    def extract_tables(self, page_no:int):
        if not self.doc:
            raise ValueError("PDF document is not opened.")
        page_no = page_no - 1
        if page_no < 0 or page_no >= self.total_pages:
            raise ValueError("Invalid page number.")

        extracted_dict = {
            'page_no': page_no,
            'extracted_text': None,
            'type': 'table_extraction'
        }

        page = self.doc[page_no]
        tabs = page.find_tables()

        if tabs.tables:
            extracted_dict['extracted_text'] = tabs[0].extract()
            self.pdf_data.append(extracted_dict)
        return extracted_dict


    def close_pdf(self):
        if self.doc:
            self.doc.close()
