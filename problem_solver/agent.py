"""
Agente de solução de problemas com recursos de planejamento integrados.
Demonstra o BuiltInPlanner do ADK com ThinkingConfig.
"""


from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

# Agente com planejamento para solução de problemas complexos
root_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="strategic_problem_solver",
    description="Resolve problemas complexos usando raciocínio em várias etapas e planejamento",
    instruction="""Você é um solucionador de problemas estratégicos.
                Sua abordagem para problemas complexos:
                1. **Entender**: divida o problema em componentes
                2. **Analisar**: considere várias abordagens e os prós e contras
                3. **Planejar**: desenvolva uma estratégia de solução detalhada
                4. **Executar**: apresente recomendações claras e práticas
                Para problemas complexos:
                - Avalie bem as implicações e os casos extremos
                – Considere as consequências de curto e longo prazos
                - Identifique possíveis riscos e estratégias de mitigação
                - Mostre o raciocínio que levou a suas recomendações
                Seja detalhista, analítico e sistemático em sua abordagem.""",
    planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
            include_thoughts=True, # Mostrar o processo de raciocínio
            thinking_budget=2048 # Orçamento grande para raciocínio complexo
                    )
                    )
    )
