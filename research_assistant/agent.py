"""
Agente assistente de pesquisa
Demonstra a ferramenta de Pesquisa Google integrada ao ADK para recuperar informações
em tempo real.
Referência: https://google.github.io/adk-docs/tools/built-in-tools#google-search
"""
from google.adk.agents import LlmAgent
from google.adk.tools import google_search # Importar a ferramenta Pesquisa Google

# Criar um assistente de pesquisa com a Pesquisa Google
root_agent = LlmAgent(
    model='gemini-3-flash-preview',  # É necessário usar o Gemini 2.0 ou superior para google_search
    name='research_assistant',
    description='Ajuda os usuários a pesquisar tópicos usando a Pesquisa Google.',
    instruction="""
    Você é um assistente de pesquisa que ajuda os usuários a encontrar informações
    precisas e atualizadas.
    Sua abordagem:
    1. Quando os usuários fizerem perguntas que exigirem informações atualizadas, use a Pesquisa Google
    2. Baseie suas respostas nos resultados da pesquisa
    3. Ao fornecer informações, cite as fontes
    4. Se os resultados da pesquisa forem insuficientes, reconheça as limitações
    Priorize sempre a acurácia em detrimento da especulação. Se não tiver certeza, diga isso.
""",
tools=[google_search] # Ativar o embasamento da Pesquisa Google
)