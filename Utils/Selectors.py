from builtins import list, dict, zip
import streamlit as st
from Utils.Get_Link import get_link

def format_item_display(row):
    """
    Formats the item display string.
    
    :param row: A row of the DataFrame.
    :return: Formatted string combining ITEM_ID, SKU, and TITLE.
    """
    return f"{row['ITEM_ID']} - {row['SKU']} - {row['TITLE']}"

def create_item_options(df):
    """
    Creates a dictionary mapping SKUs to display names for selection.

    :param df: DataFrame with item data.
    :return: Dictionary {SKU: 'ITEM_ID - SKU - TITLE'}
    """
    return df.apply(format_item_display, axis=1).to_dict()

def select_items_to_ad(df, key=1):
    """
    Allows the user to select items for advertisements, displaying SKU, ITEM_ID, and TITLE.

    :param df: DataFrame with product data.
    :param key: Unique key for Streamlit widget state.
    :return: DataFrame with selected items and generated links.
    """
    if df.empty:
        st.warning("Nenhum item disponível para seleção.")
        return df

    # Generate display names for selection
    df['item_display'] = df.apply(format_item_display, axis=1)
    item_options = dict(zip(df['SKU'], df['item_display']))

    # User selection widget
    st.write("### Selecione os itens adicionados para anúncios:")
    selected_display_names = st.multiselect(
        label="Nome, SKU ou código Mercado Livre",
        options=list(item_options.values()),
        key=key,
        placeholder="Pesquisar por Nome, SKU ou código Mercado Livre",
        label_visibility="collapsed"
    )

    # Map selected display names back to SKUs
    selected_skus = [
        sku for sku, display_name in item_options.items() if display_name in selected_display_names
    ]

    # Filter selected items
    selected_items_df = df[df['SKU'].isin(selected_skus)]

    # Generate URLs for selected items
    selected_items_df = get_link(selected_items_df)

    # Display selected items in an editable table with URLs and images
    if not selected_items_df.empty:
        st.data_editor(
            selected_items_df,
            column_config={
                "URL": st.column_config.LinkColumn(),
                "ITEM_LINK": st.column_config.LinkColumn(display_text="Editar Anúncio"),
                "IMG": st.column_config.ImageColumn("Preview", help="Visualização do item", width=90)
            }
        )
    else:
        st.info("Nenhum item selecionado.")

    return selected_items_df
