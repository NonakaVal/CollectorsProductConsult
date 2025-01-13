import requests
from builtins import str

# ------------------------- URL Shortening ------------------------- #

def shorten_url(url, timeout=10):
    """
    Shortens a URL using the TinyURL API.
    
    :param url: The URL to be shortened.
    :param timeout: Timeout for the API request.
    :return: Shortened URL or an error message.
    """
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    try:
        response = requests.get(api_url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Erro ao encurtar a URL: {str(e)}"

def shorten_links_in_df(df, link_column="URL"):
    """
    Shortens URLs in a specified DataFrame column.
    
    :param df: DataFrame containing URLs.
    :param link_column: The column name with URLs to shorten.
    :return: DataFrame with shortened URLs.
    """
    if link_column in df.columns:
        df[link_column] = df[link_column].apply(shorten_url)
    return df

# ------------------------- Link Generation ------------------------- #

def generate_product_link(item_id, title):
    """
    Generates a product URL based on ITEM_ID and TITLE.
    
    :param item_id: Unique item identifier.
    :param title: Item title.
    :return: Generated URL string.
    """
    formatted_title = title.replace(' ', '-').lower()
    return f"https://www.collectorsguardian.com.br/{item_id[:3]}-{item_id[3:]}-{formatted_title}-_JM#item_id={item_id}"

def generate_edit_link(item_id):
    """
    Generates an editable product search URL for Mercado Livre.
    
    :param item_id: Unique item identifier.
    :return: Generated URL string.
    """
    return f"https://www.mercadolivre.com.br/anuncios/lista?filters=OMNI_ACTIVE|OMNI_INACTIVE|CHANNEL_NO_PROXIMITY_AND_NO_MP_MERCHANTS&page=1&search={item_id}"

# ------------------------- Data Processing ------------------------- #

def get_link(data):
    """
    Generates product URLs and shortens them for display.
    
    :param data: DataFrame with product data.
    :return: Updated DataFrame with shortened URLs.
    """
    if data.empty:
        return data

    # Generate product URLs
    data['URL'] = data.apply(lambda row: generate_product_link(row['ITEM_ID'], row['TITLE']), axis=1)

    # Select relevant columns
    selected_columns = ["IMG", "ITEM_ID", "SKU", "TITLE", "MSHOPS_PRICE", "URL", "ITEM_LINK", "DESCRIPTION", "CATEGORY"]
    data = data[selected_columns]

    # Shorten URLs
    data = shorten_links_in_df(data, link_column='URL')

    return data

def get_link_edit(data):
    """
    Generates editable product URLs without shortening.
    
    :param data: DataFrame with product data.
    :return: Updated DataFrame with edit URLs.
    """
    if data.empty:
        return data

    # Generate edit URLs
    data['URL'] = data['ITEM_ID'].apply(generate_edit_link)

    return data
