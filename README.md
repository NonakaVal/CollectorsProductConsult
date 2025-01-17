﻿# Tabela de Consulta de Produtos

Este projeto é uma aplicação em Python desenvolvida com Streamlit para facilitar a consulta, pesquisa, e seleção de itens a partir de uma tabela de produtos. A aplicação também permite a geração de relatórios personalizados com base nos itens selecionados.

![Imgur](https://i.imgur.com/hQgCXxv.png)

![Imgur](https://i.imgur.com/x8SQCD1.png)

---

## Funcionalidades

1. **Consulta e Pesquisa**:
   - Visualize os produtos em formato de tabela.
   - Realize buscas por palavra-chave (ex.: título ou SKU).
   - Filtragem automática de resultados.
   - Exibição de estatísticas gerais, como valor total, item mais caro e item mais barato.

2. **Criação de Lista de Seleção de Itens**:
   - Selecione itens com base no SKU ou título.
   - Calcule valores totais dos itens selecionados.
   - Gere relatórios de saída com informações detalhadas.

3. **Gerenciamento de Relatórios**:
   - Exporte relatórios detalhados de itens selecionados.
   - Download direto do relatório em formato `.txt`.

---

## Integração e Processamento de dados

Os dados carregados no app são hospedados em tabelas do google e sincronizados atraves do [Streamlit GSheetsConnection](https://github.com/streamlit/gsheets-connection), 
O tratamentos usados para normalização dos dados exportados das plataformas de vendas estão em [CollectorsJupyterLab](https://github.com/NonakaVal/CollectorsJupyterLab)





## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
