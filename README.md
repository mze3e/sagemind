# BLUEPRINT Agent Builder (Streamlit + smolagents)

An MVP app to design and test agent specs with BLUEPRINT sections, then generate prompt + smolagents code.

## Features (MVP)
- BLUEPRINT Builder wizard sections
- BLUEPRINT scorecard (0-100)
- Prompt generator (`system_prompt.md`)
- smolagents code generator (`smolagents_app.py`)
- Basic tool builder with permission levels
- Local test panel (simulation)
- Version storage in SQLite
- Export center (JSON / Markdown / Python)

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```text
blueprint-agent-builder/
  app.py
  schemas/
    blueprint_schema.py
  generators/
    prompt_generator.py
    smolagents_generator.py
  tools/
    tool_builder.py
  storage/
    db.py
  templates/
    system_prompt.jinja
    smolagent_code.jinja
  exports/
  README.md
  requirements.txt
  .env.example
```

## Guardrails included
- Human approval rules are part of spec and scorecard
- Memory policy included and defaults to non-sensitive retention
- Tool permission level tracked for each tool
- Note: runtime sandbox enforcement is not implemented in MVP
