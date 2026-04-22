import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import os

st.set_page_config(page_title="Скенер за съставки", page_icon="🚫")
st.title("🔍 Проверка на съставки")

BAD_INGREDIENTS = ["E102", "E104", "E110", "E120", "E122", "E123", "E124", "E127", "E129", "E131", "E132", "E133", "E142", "E150", "E151", "E210", "E211", "E212", "E213", "E220", "E221", "E222", "E223", "E224", "E225", "E226", "E227", "E228", "E249", "E250", "E251", "E252", "E310", "E311", "E312", "E320", "E321", "E621", "E950", "E951", "E952", "E954"]

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'], gpu=False, model_storage_directory='.')

reader = load_reader()

uploaded_file = st.file_uploader("Качете снимка на етикета...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качена снимка', use_container_width=True)
    
    with st.spinner('Разпознаване на текст... моля изчакайте.'):
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0)
        full_text = " ".join(results).lower()
        
    st.subheader("Резултати от анализа:")
    
    found_bad = [ing for ing in BAD_INGREDIENTS if ing.lower() in full_text]
            
    if found_bad:
        st.error(f"⚠️ Внимание! Намерени съставки: {', '.join(found_bad)}")
    else:
        st.success("✅ Не са открити вредни съставки от списъка.")

    with st.expander("Виж целия разпознат текст"):
        st.write(full_text)
