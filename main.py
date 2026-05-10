import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agent.agent import agent_config_a, agent_config_b, loop_agent_1, loop_agent_5, base_agent
import warnings
import logging
import os

warnings.filterwarnings("ignore")
logging.getLogger("google").setLevel(logging.ERROR)

load_dotenv()

async def run_config(agent, config_name, queries):
    os.makedirs("logs", exist_ok=True)
    output_file = f"logs/output_{config_name}.txt"
    
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="sensor_agent",
        user_id="user1",
        session_id="session1"
    )
    runner = Runner(
        agent=agent,
        app_name="sensor_agent",
        session_service=session_service
    )
    with open(output_file, "w") as f:
        for query in queries:
            print(f"\n[{config_name}] {'='*50}\nQuery: {query}\n{'='*50}")
            f.write(f"\n{'='*50}\nQuery: {query}\n{'='*50}\n")
            message = Content(parts=[Part(text=query)], role="user")
            async for event in runner.run_async(
                user_id="user1",
                session_id="session1",
                new_message=message
            ):
                f.write(str(event) + "\n\n")
                if event.is_final_response():
                    if event.content and event.content.parts:
                        result = event.content.parts[0].text
                        print(result)
                        f.write(f"FINAL ANSWER: {result}\n")
                    else:
                        print("Agent returned no response.")
                        f.write("FINAL ANSWER: No response.\n")

async def main():
    with open("queries.txt", "r") as f:
        queries = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # await run_config(base_agent, "base", queries)
    await run_config(agent_config_a, "config_a", queries)
    await run_config(agent_config_b, "config_b", queries)
    await run_config(loop_agent_1, "loop_1", queries)
    await run_config(loop_agent_5, "loop_5", queries)

asyncio.run(main())