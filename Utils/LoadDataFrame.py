import pandas as pd
import streamlit as st
from Utils.AplyFilters import apply_filters
from Utils.GoogleSheetManager import GoogleSheetManager



def sku_to_date(sku):
    month_year = sku.split('-')[1]  # Extraindo, por exemplo, '0125' de '000-0125-0000'
    month = month_year[2:]          # Mês é os dois primeiros dígitos '01'
    year = '20' + month_year[:2]    # Ano é '20' seguido dos dois últimos dígitos, '25' formando '2025'

    return f'{year}-{month}'        # Retorna a string no formato '2025-01'


    
def load_and_process_data():
    # Get the URL of Google Sheets
    gs_manager = GoogleSheetManager()
    url = st.secrets["product_url"]

    if url:
        # Set up Google Sheets manager
        gs_manager.set_url(url)

        # Add worksheets
        gs_manager.add_worksheet(url, "ANUNCIOS")
        gs_manager.add_worksheet(url, "CATEGORIAS")
        gs_manager.add_worksheet(url, "CONDITIONS")

        # Read worksheets
        products = gs_manager.read_sheet(url, "ANUNCIOS")
        categorias = gs_manager.read_sheet(url, "CATEGORIAS")

        # Prepare data
        data = products.copy()
        data = data.drop_duplicates(subset='ITEM_ID', keep='first', inplace=False)



        # List of all columns
        data['SKU_DATE'] = data['SKU'].apply(sku_to_date)
        
        # Default columns to always display
        default_columns = [
            "IMG", "ITEM_ID", "SKU", "TITLE", 
            "MSHOPS_PRICE", "QUANTITY", "STATUS", 
        "URL", "ITEM_LINK", "DESCRIPTION", "CATEGORY","SKU_DATE"
        ]

        # Filter out default columns from the options in the multiselect
        # filtered_columns = [col for col in all_columns if col not in default_columns]

        # Widget multiselect for additional columns
        # selected_columns = st.sidebar.multiselect(
        #     "Selecione as colunas adicionais para exibição:",
        #     options=filtered_columns,
        # )

        # Combine default columns with the selected additional columns
        final_columns = default_columns

        # Ensure the final column order is respected
        select_data = data[final_columns]




        # Apply filters and categorization
        select_data = apply_filters(select_data, categorias)
        

        return select_data
    else:
        st.error("URL do Google Sheets não configurada corretamente!")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error
