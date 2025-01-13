import pandas as pd
import streamlit as st
from Utils.AplyFilters import apply_filters
from Utils.GoogleSheetManager import GoogleSheetManager

from builtins import IndexError, AttributeError

# ------------------------- Helper Functions ------------------------- #

def sku_to_date(sku):
    """
    Converts SKU to a date format 'YYYY-MM' based on its encoding.

    :param sku: SKU string in the format 'XXX-YYMM-XXXX'
    :return: Date string in the format 'YYYY-MM'
    """
    try:
        month_year = sku.split('-')[1]  # Extract 'YYMM'
        year = '20' + month_year[:2]    # Extract 'YY' and convert to 'YYYY'
        month = month_year[2:]          # Extract 'MM'
        return f'{year}-{month}'
    except (IndexError, AttributeError):
        return 'Invalid SKU'

# ------------------------- Data Loading & Processing ------------------------- #

def load_google_sheets_data(sheet_name):
    """
    Loads data from a specified Google Sheets worksheet.

    :param sheet_name: Name of the worksheet to load.
    :return: DataFrame with the sheet data.
    """
    gs_manager = GoogleSheetManager()
    url = st.secrets.get("product_url")

    if not url:
        st.error("URL do Google Sheets não configurada corretamente!")
        return pd.DataFrame()

    gs_manager.set_url(url)
    gs_manager.add_worksheet(url, sheet_name)
    return gs_manager.read_sheet(url, sheet_name)

def preprocess_product_data(products_df):
    """
    Cleans and processes the product data.

    :param products_df: Raw DataFrame with product data.
    :return: Processed DataFrame with necessary columns and SKU dates.
    """
    if products_df.empty:
        return products_df

    # Remove duplicates
    products_df = products_df.drop_duplicates(subset='ITEM_ID', keep='first')

    # Extract SKU date
    products_df['SKU_DATE'] = products_df['SKU'].apply(sku_to_date)

    # Define default columns
    default_columns = [
        "IMG", "ITEM_ID", "SKU", "TITLE",
        "MSHOPS_PRICE", "QUANTITY", "STATUS",
        "URL", "ITEM_LINK", "DESCRIPTION", "CATEGORY", "SKU_DATE"
    ]

    # Ensure the DataFrame has the required columns
    final_columns = [col for col in default_columns if col in products_df.columns]
    return products_df[final_columns]

# ------------------------- Main Function ------------------------- #

def load_and_process_data():
    """
    Loads product data, applies filters, and returns the final DataFrame.

    :return: Filtered and processed DataFrame.
    """
    # Load data from Google Sheets
    products_df = load_google_sheets_data("ANUNCIOS")
    categories_df = load_google_sheets_data("CATEGORIAS")

    if products_df.empty or categories_df.empty:
        st.error("Erro ao carregar os dados do Google Sheets!")
        return pd.DataFrame()

    # Process product data
    processed_data = preprocess_product_data(products_df)

    # Apply filters
    filtered_data = apply_filters(processed_data, categories_df)

    return filtered_data
