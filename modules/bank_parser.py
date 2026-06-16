import streamlit as st
from PIL import Image
import pymupdf # Required for PDF to image conversion
import io
import json
import os
import pandas as pd
import re
import plotly.express as px
from modules.utils.generative_ai import generate_response

def clear_data_source():
    st.session_state.bank_images = []
    st.session_state.analysis_result = None

def bank_statement_parser():
    """Streamlit interface for parsing bank statements using Google Gemini."""
    st.title("🏦 Bank Statement Parser 🤖")
    
    # Hybrid Data Source Selection
    st.subheader("Select Data Source")
    data_source = st.radio(
        "Choose your data source:", 
        ["Upload New File", "Use Masked Sample"], 
        horizontal=True,
        label_visibility="collapsed",
        on_change=clear_data_source
    )
    st.markdown("---")

    # Initialize session state for images and result
    if 'bank_images' not in st.session_state:
        st.session_state.bank_images = []
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

    if data_source == "Upload New File":
        # File Input
        uploaded_file = st.file_uploader("Upload bank statement:", type=["png", "jpg", "jpeg", "pdf"])

        if uploaded_file:
            # Reset images if a new file is uploaded
            # We use the file name to check if it's the same file to avoid redundant processing
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            if st.session_state.get('last_uploaded_file_key') != file_key:
                st.session_state.bank_images = []
                st.session_state.analysis_result = None
                st.session_state.last_uploaded_file_key = file_key
                
                try:
                    if uploaded_file.type.startswith('image'):
                        st.session_state.bank_images = [Image.open(uploaded_file)]
                    elif uploaded_file.type == 'application/pdf':
                        # Convert all pages of PDF to images
                        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
                        images = []
                        for page_index in range(len(doc)):
                            page = doc.load_page(page_index)
                            pix = page.get_pixmap()
                            img_data = pix.tobytes("png")
                            images.append(Image.open(io.BytesIO(img_data)))
                        st.session_state.bank_images = images
                        doc.close()
                    else:
                        st.error("Unsupported file type.")
                        st.session_state.bank_images = []
                except Exception as e:
                    st.error(f"Error processing file: {e}")
                    st.session_state.bank_images = []

            if st.session_state.bank_images:
                with st.expander(f"📄 View Uploaded Pages ({len(st.session_state.bank_images)})", expanded=False):
                    for i, img in enumerate(st.session_state.bank_images):
                        st.image(img, caption=f"Page {i+1}", width="stretch")

    elif data_source == "Use Masked Sample":
        if st.button("Load Masked Sample"):
            sample_pdf_path = "modules/bank_data/bank_statement_example.pdf"
            if os.path.exists(sample_pdf_path):
                try:
                    # Reuse PDF processing logic
                    doc = pymupdf.open(sample_pdf_path)
                    images = []
                    for page_index in range(len(doc)):
                        page = doc.load_page(page_index)
                        pix = page.get_pixmap()
                        img_data = pix.tobytes("png")
                        images.append(Image.open(io.BytesIO(img_data)))
                    st.session_state.bank_images = images
                    doc.close()
                    st.success("Sample PDF loaded! Now click 'Analyze Statement' to process it.")
                except Exception as e:
                    st.error(f"Error loading sample PDF: {e}")
            else:
                st.error("Sample PDF not found.")

        # Display preview if sample is loaded
        if st.session_state.bank_images:
            with st.expander(f"📄 View Masked Sample Pages ({len(st.session_state.bank_images)})", expanded=False):
                for i, img in enumerate(st.session_state.bank_images):
                    st.image(img, caption=f"Page {i+1}", width="stretch")

    # Submit Button - moved outside of if/else block
    if st.button("Analyze Statement"):
        # Explicit check for images in session state (works for both Uploaded or Loaded Sample)
        images = st.session_state.get('bank_images', [])
        
        if not images:
            st.warning("Please upload a file or load the sample first.")
            return

        with st.spinner("Analyzing all pages with Gemini..."):
            prompt = """
            You are an expert financial auditor. Carefully analyze the provided bank statement images.
            
            TASK:
            1. Identify EVERY SINGLE transaction across ALL provided pages. Do not skip any.
            2. Extract the 'Opening Balance' or 'Previous Balance' from the start of the statement.
            3. Classify if this is a 'credit' card statement or a 'debit' (checking/savings) account statement.
            4. Extract details for: Date, Transaction Description, Credit, Debit, Amount, and Balance for each transaction.
            5. Return the data as a JSON object.
            
            JSON STRUCTURE:
            {
              "statement_type": "credit" or "debit",
              "opening_balance": numeric_value_or_null,
              "transactions": [
                {
                  "date": "YYYY-MM-DD",
                  "transaction": "Full description here",
                  "credit": numeric_value_or_null,
                  "debit": numeric_value_or_null,
                  "amount": numeric_value_or_null,
                  "balance": numeric_value_or_null
                }
              ]
            }
            
            CONSTRAINTS:
            - Return ONLY the JSON object. No other text, no markdown code blocks.
            - Ensure all transactions from all pages are included in the 'transactions' array.
            - Use null for missing numeric values.
            - MANDATORY: Every transaction MUST have a valid date in YYYY-MM-DD format. Do not return null for date. If the date is missing for a transaction, infer it from surrounding transactions.
            - Standardize dates to YYYY-MM-DD format.
            """
            
            with st.expander("📝 View Analysis Prompt", expanded=False):
                st.code(prompt)
            
            # Reusing existing generate_response function from generative_ai utils
            result = generate_response(
                prompt, 
                st.session_state.bank_images, 
                model_name=st.session_state.get('selected_model')
            )
            
            # Clean JSON response (remove potential markdown wrappers)
            json_str = result.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()
            
            try:
                parsed_data = json.loads(json_str)
                # Ensure statement_type exists, default to 'debit' if missing for backward compatibility
                if 'statement_type' not in parsed_data:
                    parsed_data['statement_type'] = 'debit'
                st.session_state.analysis_result = parsed_data
                st.success("Analysis complete! Data extracted as JSON.")
            except Exception as e:
                st.error(f"Error parsing AI response as JSON: {e}")
                st.text("Raw response:")
                st.code(result)
            
    # Display results if they exist in session state
    if st.session_state.analysis_result:
        with st.expander("📊 View Analysis Results", expanded=True):
            # Convert JSON to DataFrame
            if isinstance(st.session_state.analysis_result, dict) and 'transactions' in st.session_state.analysis_result:
                df = pd.DataFrame(st.session_state.analysis_result['transactions'])
                opening_balance_val = st.session_state.analysis_result.get('opening_balance', 0)
                statement_type = st.session_state.analysis_result.get('statement_type', 'debit')
            else:
                # Fallback for old cache format
                df = pd.DataFrame(st.session_state.analysis_result)
                opening_balance_val = 0
                statement_type = 'debit'
            
            # Rename columns for display to match previous style
            display_df = df.rename(columns={
                'date': 'Date',
                'transaction': 'Transaction Description',
                'credit': 'Credit',
                'debit': 'Debit',
                'amount': 'Amount',
                'balance': 'Balance'
            })
            
            # Set Date as index for better display
            display_df['Date'] = pd.to_datetime(display_df['Date'], errors='coerce').dt.date
            display_df = display_df.set_index('Date')

            # --- Data Cleaning & Balance Calculation (Applies to Table and Chart) ---
            def clean_numeric(val):
                if pd.isna(val): return 0.0
                if isinstance(val, (int, float)): return float(val)
                val = str(val)
                val = re.sub(r'[^\d.-]', '', val)
                try: return float(val)
                except: return 0.0

            display_df['Credit'] = display_df['Credit'].apply(clean_numeric)
            display_df['Debit'] = display_df['Debit'].apply(clean_numeric)
            
            # Clean opening balance
            opening_balance = clean_numeric(opening_balance_val)
            
            # Logic: If credit card, opening balance is debit (negative). If debit card/account, opening balance is credit (positive).
            if statement_type == 'credit':
                opening_balance_sign = -1
                st.info(f"Credit Card Statement detected. Treating Opening Balance as Debit: -{opening_balance}")
            else:
                opening_balance_sign = 1
                st.info(f"Debit/Checking Statement detected. Treating Opening Balance as Credit: {opening_balance}")

            # Calculate balance if missing or if specifically requested to recalculate
            # We always recalculate if the balance column is entirely null
            if display_df['Balance'].isnull().all():
                st.info("Calculating cumulative balance from Credits and Debits...")
                net_change = display_df['Credit'] - display_df['Debit']
                
                # Starting point based on statement type
                start_balance = opening_balance * opening_balance_sign
                
                display_df['Balance'] = start_balance + net_change.cumsum()
            else:
                # Even if present, clean it
                display_df['Balance'] = display_df['Balance'].apply(clean_numeric)

            # --- 1. Visualization Logic (First) ---
            try:
                # Ensure Date is datetime for plotting
                plot_df = display_df.reset_index().copy()
                plot_df['Date'] = pd.to_datetime(plot_df['Date'], errors='coerce')
                plot_df = plot_df.dropna(subset=['Date'])
                
                if not plot_df.empty:
                    # Sort and Fill Logic
                    plot_df['original_order'] = range(len(plot_df))
                    plot_df = plot_df.sort_values(['Date', 'original_order'])
                    
                    min_date = plot_df['Date'].min()
                    max_date = plot_df['Date'].max()
                    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
                    date_df = pd.DataFrame({'Date': all_dates})
                    
                    daily_balance = plot_df.groupby('Date')['Balance'].last().reset_index()
                    merged_df = pd.merge(date_df, daily_balance, on='Date', how='left')
                    merged_df['Balance'] = merged_df['Balance'].ffill()
                    
                    st.subheader("📈 Balance Over Time")
                    
                    fig = px.line(
                        merged_df, 
                        x='Date', 
                        y='Balance', 
                        title='Account Balance Trend (Daily End-of-Day)',
                        markers=True
                    )
                    fig.update_layout(xaxis_title="Date", yaxis_title="Balance", hovermode='x unified')
                    st.plotly_chart(fig, width="stretch")
                else:
                    st.info("Not enough valid data to generate a balance chart.")
            except Exception as chart_err:
                st.write(f"Could not generate visualization: {chart_err}")

            # --- 2. Table Display (Second) ---
            st.subheader("📝 Transaction Details")
            st.dataframe(display_df, width="stretch")

            # --- 3. Download Logic (Third) ---
            try:
                csv_data = display_df.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name="bank_statement_analysis.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.write("Download as CSV is currently unavailable.")
