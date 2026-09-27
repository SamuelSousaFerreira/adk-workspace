"""
Demonstração de namespace – Mostra todos os quatro namespaces de estado
Demonstra os escopos de persistência temp:, session:, user: e app:.
Referência: https://google.github.io/adk-docs/sessions/state.md

"""

from google.adk.agents import LlmAgent

# Criar agente que utilize todos os quatro namespaces
root_agent = LlmAgent(
    model='gemini-3-flash-preview',
    name='namespace_demo',
    instruction="""
        Você é um assistente de demonstração que exibe namespaces de estado.
        === Estado do aplicativo (global para todos os usuários) ===
        Nome do app: {app:name?Namespace Demo}
        Versão do app: {app:version?1.0}
        === Estado do usuário (persiste entre sessões) ===
        Preferência do usuário: {user:theme?not set}
        === Estado da sessão (persiste nesta conversa) ===
        Tópico da conversa: {topic?not set}
        === Estado temporário (apenas no turno atual) ===
        Etapa atual: {temp:step?not set}
        Responda com uma mensagem amigável mostrando esses valores de namespace.
        """,
        output_key="response"
)