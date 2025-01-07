from builtins import  len
from PIL import Image

import streamlit as st

def gallery():
    

    # Parâmetros para tamanho das imagens e layout
    st.sidebar.header("Configurações")
    image_width = st.sidebar.slider("Largura da imagem", min_value=100, max_value=800, value=300)
    image_height = st.sidebar.slider("Altura da imagem", min_value=100, max_value=800, value=300)
    num_columns = st.sidebar.slider("Número de colunas", min_value=1, max_value=20, value=10)

    # Upload de múltiplos arquivos de imagem
    uploaded_files = st.sidebar.file_uploader("Envie suas imagens:", type=["png", "jpg", "jpeg", "bmp", "gif"], accept_multiple_files=True)

    if uploaded_files:
        st.sidebar.write(f"Encontradas {len(uploaded_files)} imagens enviadas.")
        
        # Exibindo imagens
        cols = st.columns(num_columns)  # Define o número de colunas dinamicamente
        for index, uploaded_file in enumerate(uploaded_files):
            try:
                image = Image.open(uploaded_file)
                image = image.resize((image_width, image_height))  # Redimensiona as imagens
                with cols[index % num_columns]:
                    st.image(image, caption=uploaded_file.name, use_container_width=True)
            except Exception as e:
                st.warning(f"Erro ao carregar {uploaded_file.name}: {e}")
