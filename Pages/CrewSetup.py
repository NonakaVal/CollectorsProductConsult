import sys
import time
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
import re
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Load OpenAI API Key
openai_key = st.secrets["OPENAI_API_KEY"]

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
    max_tokens=1500,
    openai_api_key=openai_key
)

# ========== Price Research Agents ==========
def create_price_research_agents(llm):
    source_validator = Agent(
        role="Validador de Fontes",
        goal="Identificar e validar sites brasileiros confiáveis para coleta de preços de produtos.",
        backstory="Especialista em identificar fontes seguras no mercado brasileiro.",
        llm=llm,
        allow_delegation=False,
        tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )

    price_researcher = Agent(
        role="Pesquisador de Preços",
        goal="Coletar preços atualizados de produtos em lojas e marketplaces brasileiros.",
        backstory="Especialista em coleta de informações completas sobre preços.",
        llm=llm,
        allow_delegation=False,
        tools=[SerperDevTool(), ScrapeWebsiteTool()],
        verbose=True
    )

    competitor_pricing_analyst = Agent(
        role="Analista de Preços da Concorrência",
        goal="Comparar e analisar preços coletados.",
        backstory="Especialista em análise de mercado brasileiro.",
        llm=llm,
        allow_delegation=True,
        tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )

    promotion_tracker = Agent(
        role="Rastreador de Promoções",
        goal="Rastrear promoções e descontos aplicáveis ao produto.",
        backstory="Especialista em promoções do mercado brasileiro.",
        llm=llm,
        allow_delegation=False,
        tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )

    return [source_validator, price_researcher, competitor_pricing_analyst, promotion_tracker]


# ========== Price Research Tasks ==========
def create_price_research_tasks(product_name, manufacturer, edition, agents):
    source_validation_task = Task(
        description=f"Valide sites para coletar preços do produto '{product_name}', fabricado por '{manufacturer}', edição '{edition}'.",
        expected_output="Lista de sites confiáveis.",
        agent=agents[0]
    )

    price_research_task = Task(
        description=f"Colete preços atualizados do produto '{product_name}', fabricado por '{manufacturer}', edição '{edition}'.",
        expected_output="Lista de preços com links.",
        agent=agents[1],
        context=[source_validation_task]
    )

    price_comparison_task = Task(
        description=f"Compare preços coletados do produto '{product_name}'.",
        expected_output="Relatório comparativo.",
        agent=agents[2],
        context=[price_research_task]
    )

    promotion_tracking_task = Task(
        description=f"Rastreie promoções para o produto '{product_name}'.",
        expected_output="Lista de promoções.",
        agent=agents[3],
        context=[price_research_task]
    )

    final_summary_task = Task(
        description=f"Compile todas as informações sobre o produto '{product_name}'.",
        expected_output="Relatório final consolidado.",
        agent=agents[2],
        context=[price_comparison_task, promotion_tracking_task]
    )

    return [source_validation_task, price_research_task, price_comparison_task, promotion_tracking_task, final_summary_task]


# ========== Run Price Research Crew ==========
def create_crewai_setup(product_name, manufacturer, edition):
    agents = create_price_research_agents(llm)
    tasks = create_price_research_tasks(product_name, manufacturer, edition, agents)

    product_crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=False,
        process=Process.sequential
    )
    result = product_crew.kickoff()
    return result


# ========== Console Output Redirector ==========
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []

    def write(self, data):
        # Remove ANSI escape codes
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains "Final Answer" and extract it
        final_answer_match = re.search(r"(Final Answer:|Resposta Final:)(.*)", cleaned_data, re.IGNORECASE | re.DOTALL)
        
        if final_answer_match:
            # Extract only the "Final Answer"
            final_answer = final_answer_match.group(2).strip()
            self.expander.markdown(f"**📌 Final Answer:**\n\n{final_answer}", unsafe_allow_html=True)

    def flush(self):
        pass



# ========== Streamlit Interface ==========
def run_crewai_app():
   
    


    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_name = st.text_input("Enter the product name:")
    with col2:
        manufacturer = st.text_input("Enter the manufacturer name:")
    with col3:    
        edition = st.text_input("Enter the product edition or version:")

    if st.button("Run Analysis"):
        if not product_name or not manufacturer or not edition:
            st.warning("Please fill in all fields before running the analysis.")
            return

        stopwatch_placeholder = st.empty()
        start_time = time.time()


        sys.stdout = StreamToExpander(st)
        with st.spinner("Generating Results..."):
            result = create_crewai_setup(product_name, manufacturer, edition)

        end_time = time.time()
        total_time = end_time - start_time
        stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")

        st.header("Analysis Results:")
        st.markdown(result)

run_crewai_app()
