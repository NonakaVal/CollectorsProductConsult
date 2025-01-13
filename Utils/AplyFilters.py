import streamlit as st
from Utils.Get_Link import get_link_edit

# Get the URL of Google Sheets
url = st.secrets["product_url"]

# ------------------------- Filter Functions ------------------------- #

def filter_by_column(df, column, selections):
    """Generic filter for DataFrame based on column and selected values."""
    return df[df[column].isin(selections)] if selections else df

def filter_by_status(df, status):
    """Filter DataFrame by status."""
    return df if status == "Todos" else df[df['STATUS'] == status]

def filter_by_quantity(df, min_qty, max_qty):
    """Filter DataFrame by quantity range."""
    return df[(df['QUANTITY'] >= min_qty) & (df['QUANTITY'] <= max_qty)]

def filter_by_date_range(df, selected_dates):
    """Filter DataFrame by selected dates."""
    return df[df['SKU_DATE'].isin(selected_dates)] if selected_dates else df

# ------------------------- Apply Filters ------------------------- #

def apply_filters(df, categories_df):
    """Apply all filters to the DataFrame based on user selections."""
    df_filtered = df.copy()

    # ---- Columns for Filters ---- #
    col1, col2, col3, col4 = st.columns(4)

    # ---- Status Filter ---- #
    with col1:
        selected_status = st.selectbox("Status", ['Todos', 'Ativo', 'Inativo'], index=1)
        df_filtered = filter_by_status(df_filtered, selected_status)

   
    with col2:
    # ---- Category Filter ---- #
        all_categories = categories_df['CATEGORY'].unique().tolist()
        selected_categories = st.multiselect("Categoria", all_categories)
        df_filtered = filter_by_column(df_filtered, 'CATEGORY', selected_categories)



  
    with col3:
         # ---- Quantity Filter ---- #
        min_quantity = st.number_input("Quantidade mínima", min_value=0, value=1, step=1)
        max_quantity = min_quantity + 10
        df_filtered = filter_by_quantity(df_filtered, min_quantity, max_quantity)
    with col4:
        # ---- Date Filter ---- #   
        all_dates = df['SKU_DATE'].unique().tolist()
        selected_dates = st.multiselect("Data de cadastro no SKU", all_dates)
        df_filtered = filter_by_date_range(df_filtered, selected_dates)


    # # ---- Subcategory Filter ---- #
    # all_subcategories = df['SUBCATEGORY'].unique().tolist()
    # selected_subcategories = st.multiselect("Subcategoria", all_subcategories)
    # df_filtered = filter_by_column(df_filtered, 'SUBCATEGORY', selected_subcategories)

    # # ---- Condition Filter ---- #
    # all_conditions = df['CONDITION'].unique().tolist()
    # selected_conditions = st.multiselect("Condição", all_conditions)
    # df_filtered = filter_by_column(df_filtered, 'CONDITION', selected_conditions)

    # # ---- Edition Filter ---- #
    # all_editions = df['EDITION'].unique().tolist()
    # selected_editions = st.multiselect("Edição", all_editions)
    # df_filtered = filter_by_column(df_filtered, 'EDITION', selected_editions)

    # ---- Apply Link Edit ---- #
    df_filtered = get_link_edit(df_filtered)

    return df_filtered
