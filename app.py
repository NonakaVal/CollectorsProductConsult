import streamlit as st


st.set_page_config(page_title="Consulta de Produtos", page_icon="🎮", layout='wide')

# Navegação de páginas
home = st.Page("Pages/home.py", title="Home", icon=":material/home:", default=True)

products = st.Page("Pages/Products.py", title="Consultar Produtos", icon=":material/dashboard:")

gallery = st.Page("Pages/Gallery.py", title="Ver Pastas de Imagens", icon="🖼️")


log = st.Page("Pages/log.py", title="TestLog", icon="⚙️")


pg = st.navigation(
    {
        # "Controle": [], 
        # "Home" : [home],
        "": [home],
        "Produtos": [products, gallery],
      
        
    }
)

pg.run()

