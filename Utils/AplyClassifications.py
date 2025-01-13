import pandas as pd
import json
import re
import streamlit as st

from builtins import isinstance, str, max , len, int, open


# ------------------------- Load JSON Files ------------------------- #

def load_json(file_path):
    """Utility to load JSON data from a file."""
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

edition_keywords = load_json('utils/json/editions_keywords.json')
detailed_keywords = load_json('utils/json/detailed_keywords.json')

# ------------------------- Classification Functions ------------------------- #

def flatten_keywords(keywords_dict):
    """Flatten nested keyword dictionaries into a subcategory-keywords mapping."""
    flat_keywords = {}
    for category, subcategories in keywords_dict.items():
        for subcategory, words in subcategories.items():
            key = f"{category}-{subcategory}"
            flat_keywords.setdefault(key, []).extend(words)
    return flat_keywords

def classify_items(df):
    """Classify items into subcategories based on keywords."""
    flat_keywords = flatten_keywords(detailed_keywords)

    def classify_item(title):
        if isinstance(title, str):
            item_lower = title.lower()
            matched_subcategories = [
                subcategory for subcategory, words in flat_keywords.items()
                if re.search(r'\b(?:' + '|'.join(re.escape(word.lower()) for word in words) + r')\b', item_lower)
            ]
            return max(matched_subcategories, key=len) if matched_subcategories else "Outros"
        return "Outros"

    df['SUBCATEGORY'] = df['TITLE'].apply(classify_item)
    return df

def classify_editions(df):
    """Classify items into editions based on keywords."""
    def classify_edition(title):
        if isinstance(title, str):
            item_lower = title.lower()
            for edition, words in edition_keywords.items():
                if re.search('|'.join(re.escape(word.lower()) for word in words), item_lower):
                    return edition.upper()
        return "Outros"

    df['EDITION'] = df['TITLE'].apply(classify_edition)
    return df

# ------------------------- Data Merging Functions ------------------------- #

def merge_with_condition(data, condition_df):
    """Merge condition data into the main DataFrame."""
    merged = pd.merge(data, condition_df[['ITEM_ID', 'CONDITION']], on='ITEM_ID', how='left')
    merged['CONDITION'] = merged['CONDITION'].fillna('-')
    return merged

def merge_with_categories(data, categories_df):
    """Map category names to their IDs and merge into the main DataFrame."""
    categories_df['ID'] = categories_df['ID'].apply(lambda x: f'{int(x):03d}')
    category_map = categories_df.set_index('CATEGORY')['ID'].to_dict()

    if 'CATEGORY' in data.columns:
        data['CATEGORY_ID'] = data['CATEGORY'].map(category_map)

    return data

# ------------------------- Streamlit Display Functions ------------------------- #

def display_column_data(filtered_df, column_name, title):
    """Display value counts of a DataFrame column in Streamlit."""
    st.write(title)
    if column_name in filtered_df.columns:
        counts_df = (
            filtered_df[column_name]
            .dropna()
            .value_counts()
            .reset_index()
            .rename(columns={'index': column_name.capitalize(), column_name: 'Contagem'})
        )
        counts_html = counts_df.to_html(index=False, escape=False, header=False)
        st.markdown(counts_html, unsafe_allow_html=True)
    else:
        st.error(f"Coluna '{column_name}' não encontrada no DataFrame filtrado!")

# ------------------------- Optional Image Merging (Commented) ------------------------- #

# def merge_with_images(data, images_df):
#     """Merge image URLs into the main DataFrame."""
#     merged = pd.merge(data, images_df[['ITEM_ID', 'IMG']], on='ITEM_ID', how='left')
#     merged['IMG'] = merged['IMG'].fillna('-')
#     return merged
