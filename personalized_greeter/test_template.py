"""
Teste a modelagem de estado com diferentes valores de estado.
Execute com: python test_templating.py
"""

import asyncio

from dotenv import load_dotenv

load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


async def main():
    # Configuração
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="greeter_app",
        user_id="user1",
        session_id="session1"
    )
    runner = Runner(
        agent=root_agent,
        app_name="greeter_app",
        session_service=session_service
    )

    # Teste 1: nenhum estado definido (todos os valores padrão)
    print("=== Teste 1: sem estado (todos os valores padrão) ===")
    result1 = runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=Content(parts=[Part(text="Olá")])
    )
    async for event in result1:
        if event.is_final_response():
            print(f"Agent: {event.content.parts[0].text}\n")

    # Teste 2: definir apenas o nome de usuário
    print("=== Teste 2: com nome de usuário ===")
    session.state["user_name"] = "Alex"
    result2 = runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=Content(parts=[Part(text="Olá de novo")])
    )
    async for event in result2:
        if event.is_final_response():
            print(f"Agent: {event.content.parts[0].text}\n")

    # Teste 3: definir todos os valores de estado
    print("=== Teste 3: com todos os valores de estado ===")
    session.state["user_name"] = "Alex"
    session.state["user_language"] = "espanhol"
    session.state["membership_tier"] = "premium"
    result3 = runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=Content(parts=[Part(text="Hola de nuevo")])
    )
    async for event in result3:
        if event.is_final_response():
            print(f"Agent: {event.content.parts[0].text}\n")
    print("=== Estado atual ===")
    print(session.state)


if __name__ == "__main__":
    asyncio.run(main())