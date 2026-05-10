import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agent.agent import root_agent
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("google").setLevel(logging.ERROR)

load_dotenv()

async def main():
    with open("queries.txt", "r") as f:
        queries = [line.strip() for line in f if line.strip()]
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="sensor_agent",
        user_id="user1",
        session_id="session1"
    )
    runner = Runner(
        agent=root_agent,
        app_name="sensor_agent",
        session_service=session_service
    )
    for query in queries:
        print(f"\n{'='*50}\nQuery: {query}\n{'='*50}")
        message = Content(parts=[Part(text=query)], role="user")
        
        with open("output.txt", "w") as f:
            async for event in runner.run_async(
                user_id="user1",
                session_id="session1",
                new_message=message
            ):
                f.write(str(event) + "\n\n")
                if event.is_final_response():
                    result = event.content.parts[0].text
                    print(result)

asyncio.run(main())