
import streamlit as st
from Utils.LoadDataFrame import load_and_process_data
from Utils.Selectors import select_items_to_ad
from Utils.GoogleSheetManager import GoogleSheetManager
from Utils.Reports import generate_report
import datetime
from Utils.galery import gallery



st.write("# Tabela de Consulta de Produtos")
st.write("Em caso de erro apenas atualize a página. F5")

tab1, tab2 = st.tabs(["Consulta  e Pesquisa", "Criar lista de Seleção de Itens"])

with tab1:
    # Em algum lugar no seu código
    data = load_and_process_data()

    ##############################################################################################
    # Função de Pesquisa por Correspondência de Palavras
    ##############################################################################################

    col1, col2 = st.columns([1, 2])
    with col1:
        def search_items(data, search_term):
            """
            Filtra o DataFrame para itens que contenham o termo de pesquisa em qualquer coluna de texto.
            """
            if search_term:
                # Filtra o DataFrame baseado na correspondência do termo de pesquisa nas colunas 'TITLE' e 'SKU'
                filtered_data = data[data.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
            else:
                # Se não houver termo de pesquisa, retorna o DataFrame completo
                filtered_data = data
            return filtered_data


        st.write("#### Pesquisar por palavra-chave")

        search_term = st.text_input("Pesquisar por palavra-chave")

    # Filtra os dados com base no termo de pesquisa
    searched_data = search_items(data, search_term)

    st.dataframe(
    searched_data,
    column_config={
        "URL": st.column_config.LinkColumn(display_text="Link do Produto"),
        "ITEM_LINK": st.column_config.LinkColumn(display_text="Editar Anúncio"),
        "IMG": st.column_config.ImageColumn(
            "Preview", help="Preview da imagem", width=130
        )
    }
    )

    shape = data.shape

    st.write(f"Total de Itens: {shape[0]}")

with tab2:

##############################################################################################
# Função para selecionar itens do Google Sheets
##############################################################################################
    
    def select_items(data):
        # Criar uma coluna para exibição combinada de SKU e TITLE
        data['item_display'] = data['ITEM_ID'].astype(str) + ' - ' + data['SKU'].astype(str) + ' - ' + data['TITLE']

        # Criar uma caixa de seleção múltipla para escolher itens
        item_options = data[['SKU', 'item_display']].set_index('SKU')['item_display'].to_dict()
        selected_display_names = st.multiselect("Selecione os itens (SKU - Nome)", options=list(item_options.values()))

        # Mapear nomes de exibição selecionados de volta para SKU
        selected_skus = [key for key, value in item_options.items() if value in selected_display_names]

        # Filtrar o DataFrame para obter as linhas correspondentes
        selected_items_df = data[data['SKU'].isin(selected_skus)]

        # Exibir o DataFrame dos itens selecionados
        if not selected_items_df.empty:
            st.write("Itens selecionados:")
            st.dataframe(selected_items_df[['ITEM_ID', 'SKU', 'TITLE']])

        return selected_items_df


##############################################################################################
# Função principal do Streamlit
##############################################################################################

# st.write("#### Criar lista de itens com links encurtados")

    select = select_items_to_ad(data)
    



##############################################################################################
##############################################################################################

    if not select.empty:

        # Calcula o número total de itens
        total_items = select['CATEGORY'].value_counts().sum()
        
        # Remover formatação do preço e convertê-lo para inteiro
        select['MSHOPS_PRICE'] = select['MSHOPS_PRICE'].str.replace('R$', '', regex=False).str.replace(',00', '', regex=False).str.replace('.', '', regex=False).str.strip()
        select['MSHOPS_PRICE'] = select['MSHOPS_PRICE'].astype(int)

        # Soma total dos preços e formatação
        price_counts = select["MSHOPS_PRICE"].sum()
        formatted_price = f"R$ {price_counts:,.2f}"

        st.write(f"Total de Itens: {total_items}")
        st.write(f"Valor Total: {formatted_price}")

        # Gerar o relatório de saída
        report_path = generate_report(select, config={})  # Configurar conforme necessário
        st.write(f"Relatório de Saída gerado em: {report_path}")

        # Criar o botão de download
        with open(report_path, "rb") as file:
            st.download_button(
                label="Gerar Registro de Saída",
                data=file,
                file_name=f"Registro_de_saida_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
                mime="text/plain"
            )
