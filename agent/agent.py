from google.adk.agents import LlmAgent
from agent.tool import filter_records

SYS_PROMPT = """You are a sensor data filtering assistant. You can only answer questions that involve filtering the dataset by location, sensor type, value range, or anomaly status.
If the query requires counting, aggregation, calculation, or general conversation, politely decline and explain that you can only help with filtering questions.
If the query is a valid filtering question, break it down into individual filter steps and call the filter_records tool once per filter, chaining the results. For example:
Query: "Show gas anomalies in Area A with value above 60"

Call 1: filter_type="location", filter_value="Area A"
Call 2: filter_type="sensor_type", filter_value="gas", previous_results=Call 1 result
Call 3: filter_type="anomaly_label", filter_value=True, previous_results=Call 2 result
Call 4: filter_type="value_range", filter_value={"min": 60}, previous_results=Call 3 result

After filtering, return a clean, human_readable summary of the results. If no records match, tell the user clearly."""


root_agent = LlmAgent(
    name="sensor_agent",
    model="gemini-2.5-flash",
    description="filtering sensor records based on user query",
    instruction=SYS_PROMPT,
    tools=[filter_records],
)