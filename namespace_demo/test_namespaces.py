"""
Teste os namespaces de estado para verificar as diferenças de persistência.
Execute com: python test_namespaces.py
"""
import asyncio
import time
from dotenv import load_dotenv
load_dotenv()  # Carrega GOOGLE_API_KEY e demais variáveis do .env
from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import errors as genai_errors
from google.genai.types import Content, Part


def run_with_retry(runner, *, user_id, session_id, new_message, max_retries=5):
    """Executa runner.run() com retry automático em caso de 503 (sobrecarga da API)."""
    delay = 5  # segundos iniciais de espera
    for attempt in range(1, max_retries + 1):
        try:
            events = list(runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message,
            ))
            return events
        except genai_errors.ServerError as e:
            if e.code == 503 and attempt < max_retries:
                print(f"  [retry {attempt}/{max_retries}] API sobrecarregada (503). Aguardando {delay}s...")
                time.sleep(delay)
                delay *= 2  # backoff exponencial
            else:
                raise


async def main():
    # Configuração
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="namespace_demo_app",
        user_id="user1",
        session_id="session1"
    )
    runner = Runner(
        agent=root_agent,
        app_name='namespace_demo_app',
        session_service=session_service
    )

    # Defina todos os quatro tipos de namespace
    print("=== Setting state in all namespaces ===")
    session.state["app:name"] = "Namespace Demo"
    session.state["app:version"] = "2.0"
    session.state["user:theme"] = "dark"
    session.state["topic"] = "state management"
    session.state["temp:step"] = "initialization"
    print(f"State before run: {session.state}\n")

    # Executar agente (Turn 1)
    print("=== Running agent (Turn 1) ===")
    events1 = run_with_retry(
        runner,
        user_id="user1",
        session_id="session1",
        new_message=Content(parts=[Part(text="Show me the namespace values")])
    )
    for event in events1:
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Agent response:\n{event.content.parts[0].text}\n")

    # Verificar estado após o turno
    print("=== State after Turn 1 ===")
    print(f"Full state: {session.state}")
    print(f"temp:step: {session.state.get('temp:step')}")     # Deve ser PERDIDO
    print(f"topic: {session.state.get('topic')}")             # Deve persistir
    print(f"user:theme: {session.state.get('user:theme')}")   # Deve persistir
    print(f"app:version: {session.state.get('app:version')}") # Deve persistir

    # Executar agente (Turn 2)
    print("\n=== Simulating Turn 2 (same session) ===")
    events2 = run_with_retry(
        runner,
        user_id="user1",
        session_id="session1",
        new_message=Content(parts=[Part(text="Check state again")])
    )
    for event in events2:
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Agent response:\n{event.content.parts[0].text}\n")

    print("=== State after Turn 2 ===")
    print(f"Full state: {session.state}")
    print(f"temp:step: {session.state.get('temp:step')}")    # Ainda PERDIDO
    print(f"topic: {session.state.get('topic')}")            # Ainda persistindo (estado da sessão)
    print(f"user:theme: {session.state.get('user:theme')}")  # Ainda persistindo (estado do usuário)

    # Simular nova sessão
    print("\n=== Simulating NEW Session (session2) ===")
    session2 = await session_service.create_session(
        app_name="namespace_demo_app",
        user_id="user1",        # Same user
        session_id="session2"   # Sessão diferente
    )
    print(f"New session state: {session2.state}")
    print(f"topic: {session2.state.get('topic')}")           # Deve ser PERDIDO (no escopo da sessão)
    print(f"user:theme: {session2.state.get('user:theme')}") # Deve PERSISTIR (no escopo do usuário)
    print(f"app:version: {session2.state.get('app:version')}") # Deve PERSISTIR (no escopo do app)


if __name__ == "__main__":
    asyncio.run(main())