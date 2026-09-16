"""
    Extrator de nomes: demonstra os conceitos básicos do estado da sessão
    Mostra como usar output_key para salvar dados e acessá-los com session.state.
    Referência: https://google.github.io/adk-docs/sessions/state.md
"""
from google.adk.agents import LlmAgent
# Agente único que extrai e salva o nome
root_agent = LlmAgent(
    model='gemini-3.5-flash',
    name='name_extractor',
    instruction="Extract the person's name from the message. Retorna SOMENTE o nome, nada mais.",
    output_key="user_name" # Salva a resposta em state["user_name"]
)
