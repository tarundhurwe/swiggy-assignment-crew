# AI Agent Evaluation Pipeline

## Overview

This project implements a **continuous evaluation pipeline for AI agents**, capable of:

- Ingesting multi-turn conversations
- Evaluating response quality, tool accuracy, and coherence
- Storing evaluation results in Postgres
- Generating actionable improvement suggestions for prompts and tools
- Exposing a Streamlit/Gradio UI for inspection

**Current Status:** All core evaluation features are functional and synchronous. Celery integration for asynchronous task processing is planned for future improvement.

---

## Architecture

- **FastAPI**: Handles ingestion (`/ingest`) and result queries (`/results/<conversation_id>`)
- **Postgres**: Stores raw conversation logs and evaluation results
- **Evaluation Logic**: Executes multi-turn and tool evaluations; generates improvement suggestions
- **Streamlit UI**: Provides interactive interface to explore results and suggestions

**Note:** Celery + Redis integration is currently omitted to focus on core functionality. Evaluation runs **synchronously** upon ingestion. This can be upgraded to async processing with minimal changes.

---

## Future Improvements

- **Asynchronous Evaluation with Celery**:
  - Offload evaluation tasks to workers for high throughput
  - Avoid blocking API calls
  - Scale easily to thousands of conversations per minute
- **Task Queue Monitoring**:
  - Track pending evaluations
  - Retry failed tasks
- **Periodic Meta-Evaluation**:
  - Auto-tune evaluators using historical results

---

## Running the Project

```bash
# Build and start the system
docker-compose up --build

# Streamlit UI (if using Streamlit)
streamlit run app/ui.py
```
