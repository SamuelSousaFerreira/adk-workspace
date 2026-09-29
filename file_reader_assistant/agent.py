"""
Agente assistente de leitura de arquivos
Demonstra a integração das ferramentas do MCP com o ADK usando o servidor MCP do
sistema de arquivos.
Referência: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Definir a pasta para permitir o acesso aos arquivos (o caminho precisa ser absoluto)
ALLOWED_PATH = os.path.abspath("./my_files")

# Criar a pasta se ela não existir
os.makedirs(ALLOWED_PATH, exist_ok=True)

# Criar o agente com as ferramentas do sistema de arquivos do MCP
root_agent = LlmAgent(
    model='gemini-3-flash-preview',
    name='file_reader_assistant',
    description='Permite que os usuários leiam e descubram arquivos usando as ferramentas do MCP.',
    instruction="""Você é um assistente de leitura de arquivos que ajuda os usuários a analisar arquivos.

Suas capacidades:
- Listar arquivos em diretórios usando list_directory
- Ler o conteúdo do arquivo usando read_file

Ao ajudar os usuários:
1. Use list_directory para exibir os arquivos disponíveis
2. Use read_file para exibir o conteúdo do arquivo quando solicitado
3. Descreva o que você encontrou de forma útil

Sempre deixe claro com qual pasta você está trabalhando.""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=[
                        '-y',
                        '@modelcontextprotocol/server-filesystem',
                        ALLOWED_PATH,
                    ],
                ),
            ),
            # Filtrar para expor apenas ferramentas seguras e somente leitura
            tool_filter=['list_directory', 'read_file'],
        )
    ],
)                   