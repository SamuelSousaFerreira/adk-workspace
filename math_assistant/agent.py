"""
Agente assistente de matemática
Demonstra a ferramenta integrada de execução de código do ADK para cálculos.
Referência: https://google.github.io/adk-docs/tools/built-in-tools#code-execution
"""
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor # Importar executor de código

# Criar um assistente de matemática com execução de código
root_agent = LlmAgent(
    model='gemini-3.1-flash-lite', # É necessário usar o Gemini 2.0 ou superior para a execução de código
    name='math_assistant',
    description='Auxilia os usuários com cálculos e análises matemáticas.',
    instruction="""
        Você é um assistente de matemática que ajuda os usuários com cálculos e análises matemáticas.
        Suas capacidades:
        1. Quando os usuários solicitarem cálculos, use a execução de código para ter precisão
2. Mostre seus cálculos explicando os passos do processo
3. Verifique os resultados executando o código
4. Realize operações matemáticas complexas (estatística, álgebra etc.)
Para garantir a acurácia dos cálculos numéricos, utilize sempre a execução de código.
""",
code_executor=BuiltInCodeExecutor() # Ativar execução de código
)
