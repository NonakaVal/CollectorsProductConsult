# from Utils.Galery import gallery

# gallery()

import streamlit as st
import pandas as pd
from io import StringIO

st.title("Upload de Arquivos")

# Permitir o upload de até 3 arquivos
uploaded_files = st.file_uploader("Escolha até 3 arquivos", accept_multiple_files=True)

if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        st.subheader(f"Arquivo {i + 1}: {uploaded_file.name}")

        # Ler o arquivo como DataFrame e exibir
        try:
            dataframe = pd.read_csv(uploaded_file)
            st.dataframe(
                dataframe,
                column_config={
                    "IMG": st.column_config.ImageColumn(
                        "Preview", help="Preview da imagem", width=300
                    )
                },
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erro ao processar o arquivo {uploaded_file.name}: {e}")
