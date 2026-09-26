"""
    Agente assistente de geografia
    Demonstra o parâmetro de ferramentas do ADK com uma ferramenta de função personalizada
    simples.
    Referência: https://google.github.io/adk-docs/agents/llm-agents#tools
"""
from google.adk.agents import LlmAgent

# Etapa 1: definir uma função de ferramenta
def get_capital_city(country: str) -> str:
    """Recupera a capital de um país específico."
    
    Args:
        country (str): o nome do país.
    
    Retorna:
        str: nome da capital ou mensagem de erro.
    """
    # Banco de dados simulado de capitais
    capitals = {
    "França": "Paris",
    "Japão": "Tóquio",
    "Canadá": "Ottawa",
    "Alemanha": "Berlim",
    "Brasil": "Brasília",
    "Austrália": "Canberra",
    "Índia": "Nova Délhi",
    "México": "Cidade do México"
    }
    
    # Consultar a capital
    return capitals.get(
        country,
        f"Desculpe, não tenho informações sobre a capital de {country}."
    )
# Etapa 2: criar um agente com a ferramenta
root_agent = LlmAgent(
    model= 'gemini-3-flash-preview',
    name='geography_assistant',
    description='Ajuda os usuários a aprender sobre geografia mundial.',
    instruction= """ Você é um assistente de geografia que ajuda os usuários a aprender sobre as capitais do mundo.
                    Quando um usuário perguntar sobre uma capital:
                    1. Use a ferramenta get_capital_city para encontrar a resposta.
                    2. Apresente as informações de forma amigável e didática.
                    3. Você pode adicionar fatos interessantes, se conhecer algum.
                    Se a ferramenta retornar uma mensagem de erro, diga educadamente ao usuário que
                    você não possui essa informação.
                    """,
tools=[get_capital_city] # Disponibilizar a função como uma ferramenta
)