# Sensor Query Agent

A single-agent system built with Google ADK that answers natural language filtering questions about a sensor dataset.

## Overview

The agent accepts natural language queries, determines if they are valid filtering questions, and applies filters sequentially using a chained tool-calling approach. It strictly declines aggregation, calculation, or general conversation queries.

## Project Structure

```
sensor-query-agent/
├── agent/
│   ├── __init__.py
│   ├── agent.py        # Agent definitions (base, config_a, config_b, loop_1, loop_5)
│   └── tool.py         # filter_records tool
├── logs/               # Output logs per configuration (generated at runtime)
│   ├── output_base.txt
│   ├── output_config_a.txt
│   ├── output_config_b.txt
│   ├── output_loop_1.txt
│   └── output_loop_5.txt
├── main.py             # Entry point
├── queries.txt         # Test queries (use # for comments)
├── sensor_data.xlsx    # Dataset
├── report.pdf          # Assignment report
└── pixi.toml
```

## Setup

### Requirements
- Python 3.11+
- [pixi](https://pixi.sh)
- Google API key (get one at https://aistudio.google.com/apikey)

### Install

```bash
git clone https://github.com/fatemehdoudi/sensor-query-agent.git
cd sensor-query-agent
pixi install
```

### Configure

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_key_here
```

## Running the Agent

```bash
pixi shell
python main.py
```

By default, `main.py` runs the **base agent** on all queries in `queries.txt`. Output logs are saved to the `logs/` folder.

To test other configurations (temperature variants, LoopAgent), uncomment the relevant lines in `main.py`:

```python
await run_config(base_agent, "base", queries)
# await run_config(agent_config_a, "config_a", queries)  # temperature=0.0
# await run_config(agent_config_b, "config_b", queries)  # temperature=1.0
# await run_config(loop_agent_1, "loop_1", queries)      # max_iterations=1
# await run_config(loop_agent_5, "loop_5", queries)      # max_iterations=5
```

## Adding Queries

Edit `queries.txt` — one query per line. Use `#` to add comments:

```
# Normal queries
Show gas readings in Area A

# Should decline
How many anomalies are in Area B?
```

## Valid Query Types

The agent only handles filtering questions. Supported filters:
- **location** — e.g. `"Show readings in Area A"`
- **sensor_type** — e.g. `"Show gas readings"`
- **value_range** — e.g. `"Show readings with value above 50"`
- **anomaly_label** — e.g. `"Show anomalies"` or `"Show readings that are not anomalies"`

## Design Decisions

- The tool applies exactly one filter per call — multi-condition queries are handled by chaining calls sequentially.
- `filter_value` for `value_range` must be a dict with optional `min`/`max` keys. If the LLM passes an unexpected type, the tool returns a descriptive error without crashing.
- The agent does not support OR-based location filtering natively — multi-location queries rely on emergent LLM behavior.

## Report

See `report.pdf` for a full discussion of agent architecture, tool design, example queries, failure cases, and execution control observations.
