import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="Скенер за вредни съставки", page_icon="🚫")
st.title("🔍 Проверка на съставки от снимка")

BAD_INGREDIENTS = [
    "621", "E621", "monosodium glutamate", "мононатриев глутамат",
    "палмово масло", "aspartame", "аспартам", "E951"
]

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'], gpu=False)

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
    
    found_bad = []
    for ingredient in BAD_INGREDIENTS:
        if ingredient.lower() in full_text:
            found_bad.append(ingredient)
            
    if found_bad:
        st.error(f"⚠️ Внимание! Намерени са потенциално вредни съставки: {', '.join(found_bad)}")
    else:
        st.success("✅ Не са открити съставки от списъка с вредни елементи.")

    with st.expander("Виж целия разпознат текст"):
        st.write(full_text)
