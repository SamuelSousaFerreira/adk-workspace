"""
Demonstração da configuração do modelo que compara a otimização factual com a
criativa.
Demonstra o generate_content_config do ADK com configurações diferentes.
"""
from google.adk.agents import LlmAgent
from google.genai import types

# Agente 1: otimizado para extração de dados factuais
# Usa temperatura baixa para consistência, segurança rigorosa para acurácia
factual_agent = LlmAgent(
    model="gemini-3.5-flash", # Flash é suficiente para extração
    name="data_extractor",
    description="Extrai informações factuais com alta consistência",
    instruction="""Você é um extrator de dados preciso.
        Extrair os fatos exatamente como estão apresentados. Não:
        - Adicionar informações que não constam na entrada
        - Fazer deduções nem inferências
        - Usar linguagem criativa
        Seja preciso, conciso e determinista.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1, # Muito baixa para consistência
        max_output_tokens=500,
        top_p=0.8,
        top_k=10,
        safety_settings=[
        types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        )
            ]
        )
)

# Agente 2: otimizado para criação de ideias inovadoras
# Usa temperatura alta para criatividade, modelo Pro para ideias melhores
creative_agent = LlmAgent(
    model="gemini-3.5-flash", # Pro para criatividade superior
    name="creative_brainstormer",
    description="Gera ideias criativas e examina as possibilidades",
    instruction="""Você é um parceiro de criação de ideias inovadoras.
                Gerar ideias variadas e cheias de imaginação. Fique à vontade para:
                - Soltar a imaginação
                - Combinar conceitos inesperados
                - Analisar abordagens pouco convencionais
                Seja criativo, diversificado e instigante.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.9, # Alta para criatividade
        max_output_tokens=2000, # Permitir ideias detalhadas
        top_p=0.95,
        top_k=40,
        safety_settings=[
            types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
        ]
        )
        )

# Para adk web, vamos usar o agente factual como root_agent
# Mudar para creative_agent para testar outro comportamento
root_agent = creative_agent