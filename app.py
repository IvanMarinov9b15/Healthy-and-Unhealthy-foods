import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import os

st.set_page_config(page_title="Скенер за съставки", page_icon="🚫")
st.title("🔍 Проверка на съставки")

BAD_INGREDIENTS = [
    "621", "e621", "monosodium glutamate", "мононатриев глутамат",
    "палмово масло", "aspartame", "аспартам", "e951"
]

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
