# 🧠 SageMind AI

**Design, test, and deploy intelligent agents — the right way.**

SageMind AI is a **Streamlit-based agent builder** that helps you create reliable, production-ready AI agents using the **BLUEPRINT framework**. Instead of trial-and-error prompt writing, SageMind guides you through a structured approach to building agents with clear goals, constraints, tools, and guardrails.

---

## 🚀 Why SageMind AI?

Most AI agents fail not because of the model — but because of poor design.

SageMind AI helps you move from:

> ❌ Prompt hacking
> ✅ Structured agent engineering

It enforces discipline through a repeatable framework so your agents are:

* Predictable
* Auditable
* Safe
* Production-ready

---

## 🏗️ Core Features

### 🧩 BLUEPRINT Agent Builder

Create agents using a structured workflow:

* Behaviour & Values
* Limitations & Non-Goals
* Use Case & Purpose
* Examples & Test Cases
* Parameters & Configuration
* Requirements
* Interfaces (Tools & Data)
* Version Control
* Temporal Memory

---

### ⚙️ smolagents Code Generation

Automatically convert your design into working agents:

* `CodeAgent` and `ToolCallingAgent` support
* Model configuration (OpenAI, Hugging Face, etc.)
* Tool integration
* Execution settings and guardrails

---

### 🛠️ Tool Builder

Define and attach tools to your agents:

* Custom Python functions
* Input/output schemas
* Permission levels (read / write / approval required)

---

### 🧪 Test Lab

Validate your agents before deploying:

* Run single or batch test cases
* Inspect reasoning steps
* Track tool usage
* Detect failures and guardrail violations

---

### 🗂️ Version Control

Track how your agent evolves:

* Version history
* Prompt diffs
* Test results per version
* Change logs

---

### 🧠 Memory Manager

Control how your agent remembers:

* No memory / session memory / persistent memory
* Transparent memory summaries
* User-controlled deletion

---

### 📦 Export Center

Export your agent as:

* Markdown system prompt
* JSON configuration
* Python (smolagents-ready)
* Streamlit app
* Docker-ready package

---

## 🖥️ App Structure

```
SageMind AI
├── Home
├── BLUEPRINT Builder
├── Tools & Interfaces
├── Prompt Preview
├── Code Generator
├── Test Lab
├── Version History
└── Export Center
```

---

## ⚡ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/sagemind-ai.git
cd sagemind-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 🧱 Tech Stack

* **Frontend:** Streamlit
* **Agent Framework:** smolagents
* **Backend:** Python
* **Schemas:** Pydantic
* **Templating:** Jinja2
* **Storage:** SQLite (local)

---

## 🔐 Guardrails & Safety

SageMind AI is designed with safety in mind:

* Tool permissions are explicit and enforced
* High-risk actions require human approval
* API keys are never embedded in prompts
* Agent outputs are structured and testable
* Clear separation between draft and production agents

---

## 🎯 Use Cases

Ideal for:

* Financial analysis agents
* Reporting and briefing automation
* Operations workflows
* Knowledge assistants
* Compliance and contract analysis
* Internal copilots for teams

---

## 🛣️ Roadmap

### v1 (Current)

* BLUEPRINT builder
* Prompt + code generation
* Test lab
* Basic tool builder
* Export functionality

### v2 (Planned)

* Multi-agent orchestration
* RAG / document upload
* Advanced evaluation dashboard
* Deployment integrations
* Team collaboration
* Agent marketplace

---

## 🤝 Contributing

Contributions are welcome.

If you want to:

* Improve the builder UX
* Add new agent templates
* Extend smolagents integrations
* Enhance testing and evaluation

Feel free to open a PR or issue.

---

## 📄 License

MIT License

---

## 💡 Philosophy

> Good agents aren’t accidents — they’re engineered.

SageMind AI exists to bring structure, discipline, and reliability to how we build AI systems.
