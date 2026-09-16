"""
Script de teste para visualizar o acesso ao estado diretamente.
Execute com: python test_state.py
"""
import asyncio

from dotenv import load_dotenv

load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


async def main():
    # Configurar a sessão e o Runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="name_extractor_app",
        user_id="test_user",
        session_id="test_session"
    )
    runner = Runner(
        agent=root_agent,
        app_name="name_extractor_app",
        session_service=session_service
    )

    # Teste: extrair o nome
    user_message = Content(parts=[Part(text="Olá, meu nome é Alex Johnson")])
    print("=== Running agent ===")
    result = runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=user_message
    )

    # Mostrar resposta final
    async for event in result:
        if event.is_final_response():
            print(f"\nAgent response: {event.content.parts[0].text}")

    # Acessar o estado de forma programática
    print(f"\n=== State after execution ===")
    print(f"Full state: {session.state}")
    print(f"Extracted name: {session.state.get('user_name')}")

    # Seu código agora pode tomar decisões com base no estado
    if session.state.get("user_name"):
        print("✅ O nome foi extraído e armazenado com sucesso!")
    else:
        print("❌ Falha na extração do nome")

    # Teste de acesso em turnos subsequentes
    print("\n=== Simulating second turn ===")
    result2 = runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=Content(parts=[Part(text="Qual é o meu nome?")])
    )
    async for event in result2:
        if event.is_final_response():
            print(f"Agent response: {event.content.parts[0].text}")
    print(f"\nState still contains: {session.state.get('user_name')}")
    print("✅ O estado persiste entre turnos!")


if __name__ == "__main__":
    asyncio.run(main())
