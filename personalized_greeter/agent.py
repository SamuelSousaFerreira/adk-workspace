
"""
Saudador personalizado  demonstra a modelagem de estado
Mostra como a modelagem de {var} injeta valores de estado nas instruções.
Referência: https://google.github.io/adk-docs/sessions/state.md
"""

from google.adk.agents import LlmAgent

# Agente com modelagem de estado
# Nota: o template do ADK suporta apenas {var} (obrigatória) e {var?} (opcional,
# vira string vazia se ausente). Não há sintaxe de valor padrão nem aninhamento.
root_agent = LlmAgent(
    model='gemini-3.5-flash',
    name='personalized_greeter',
    instruction="""
        Você é um assistente amigável.
        Informações do usuário (campos podem estar vazios):
        - Nome: {user_name?}
        - Idioma preferido: {user_language?}
        - Assinatura: {membership_tier?}

        Cumprimente o usuário cordialmente e ofereça ajuda.
        Se o nome estiver disponível, use-o na saudação.
        Se o nível de assinatura estiver disponível, mencione-o.
        Responda no idioma preferido do usuário; se não estiver definido, responda em inglês.
        """
)