import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from app.agent import root_agent

async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(user_id="test_user", app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    # First, list some logs to populate context (simulation, though the agent will fetch real logs)
    # Then ask for a chart
    query = "Please analyze recent logs and generate a chart of log severity."
    print(f"User: {query}")
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=types.Content(
            role="user", 
            parts=[types.Part.from_text(text=query)]
        ),
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")
        
        if event.get_function_calls():
            for fc in event.get_function_calls():
                print(f"Agent Tool Call: {fc.name}({fc.args})")

if __name__ == "__main__":
    asyncio.run(main())