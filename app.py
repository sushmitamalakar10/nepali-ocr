import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from streamlit_cropper import st_cropper

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(layout="wide", page_title="Nepali OCR")

st.title("Nepali OCR")
st.write("Upload image → Extract Nepali text")

# Session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None

uploaded_file = st.file_uploader("Choose JPG/PNG", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Original")
        
        if st.button("Extract Text", type="primary"):
            with st.spinner("Processing..."):
                arr = np.array(image)
                gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
                # thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
                # kernel = np.ones((2,2), np.uint8)
                # proc = cv2.dilate(thresh, kernel, iterations=2)
                
                st.session_state.extracted_text = pytesseract.image_to_string(arr, lang='nep').strip()
                st.session_state.processed_image = Image.fromarray(gray)
    
        if st.session_state.extracted_text:
            st.image(st.session_state.processed_image, caption="Processed")
            st.text_area("Nepali Text", st.session_state.extracted_text, height=300)
            st.download_button("Download TXT", st.session_state.extracted_text)

st.caption("By Sushmita Malakar")