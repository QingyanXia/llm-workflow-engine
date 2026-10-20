# LLM Workflow Engine

A **FastAPI + DeepSeek** prototype that turns natural-language requests into sequential LLM tasks. It explores task planning, context passing, and execution status tracking.

> **Status:** Experimental prototype. Steps generate text with an LLM; the app does not run shell commands or call external tools.

## Features

- Task creation, execution and retrieval through a REST API
- LLM-based feasibility and suitability checks
- Automatic decomposition into actionable steps
- Sequential step execution with prior outputs as context
- Task and step status tracking (in memory)

**Stack:** Python 3.10+, FastAPI, OpenAI SDK (DeepSeek-compatible API), Uvicorn.

## Run locally

You need Python 3.10+ and a DeepSeek API key. **Running a task uses paid API calls.**

```bash
git clone https://github.com/QingyanXia/llm-workflow-engine.git
cd llm-workflow-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows, use `.venv\Scripts\activate` and `copy .env.example .env` instead.

Set your key in `.env` (never commit it):

```dotenv
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=deepseek-v4-pro
```

The optional `DEEPSEEK_MODEL` lets you select another supported model. Refer to [DeepSeek API documentation](https://api-docs.deepseek.com/) for current model names.

Start the server:

```bash
uvicorn app.main:app --reload
```

The interactive API is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Example: create, run and inspect a task

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/task -H 'Content-Type: application/json' -d '{"input":"Create a three-day Python study plan"}'
```

Copy the `id` from the response, and substitute it for `<TASK_ID>`:

```bash
curl -X POST http://127.0.0.1:8000/task/<TASK_ID>/run
curl http://127.0.0.1:8000/task/<TASK_ID>
```

The final response contains the individual planned steps, outputs and overall status. Execution performs an LLM call for feasibility, another for planning, and one for each step.

## How it works

```text
POST /task
  -> Save a pending task
POST /task/{id}/run
  -> Check feasibility with the LLM
  -> Generate ordered steps with the LLM
  -> Execute each step with earlier results as context
  -> Update task and step statuses
GET /task/{id}
  -> Return task details and output
```

## Limitations

- In-memory task storage; data is lost when the server restarts.
- Synchronous, sequential execution; no background queue.
- No external tool execution, persistent database or RAG.
- The suitability classification is recorded but does not yet prevent execution.
- The plain-text step parser depends on the model's output format.

## Code map

- `app/api/task.py` — HTTP endpoints
- `app/core/llm.py` — DeepSeek API client
- `app/core/planner.py` — step generation
- `app/core/validator.py` — feasibility and suitability checks
- `app/services/task_service.py` — orchestration and state updates
- `app/models/` and `app/storage/` — models and in-memory storage

License: MIT.
