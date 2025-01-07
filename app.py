 

import streamlit as st

# Set page configuration
st.set_page_config(page_title="Consulta de Produtos", page_icon="🎮", layout='wide')

# Simple user authentication using st.secrets
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def authenticate_user(username, password):
    # Access credentials from st.secrets
    credentials = st.secrets["credentials"]
    return credentials.get(username) == password

# Login Form
if not st.session_state["authenticated"]:
    
   
    # Adicionar a imagem centralizada no início da página
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://i.imgur.com/Ti4ILVw.png" style="width: 10%;"/>
    </div>
                

""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.success("Login successful!")
                
            else:
                st.error("Invalid username or password.")
else:
    # Navigation and Pages
    st.sidebar.title("Menu")
    

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



