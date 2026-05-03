from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from generators.prompt_generator import render_system_prompt
from generators.smolagents_generator import render_smolagents_code
from schemas.blueprint_schema import AgentSpec, MemoryMode, PermissionLevel, TestCase, ToolSpec
from storage.db import init_db, list_versions, load_draft, list_drafts, save_draft, save_version

init_db()
st.set_page_config(page_title="BLUEPRINT Agent Builder", layout="wide")
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        }
        .hero {
            background: linear-gradient(120deg, #1e3a8a 0%, #2563eb 55%, #7c3aed 100%);
            border-radius: 1rem;
            padding: 1.2rem 1.4rem;
            color: #ffffff;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.18);
            margin-bottom: 1rem;
        }
        .capability-card {
            border: 1px solid #dbeafe;
            border-radius: 0.9rem;
            padding: 0.85rem;
            background: #ffffff;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
            margin-bottom: 0.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Streamlit BLUEPRINT Agent Builder (smolagents)")

st.sidebar.header("Project")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "BLUEPRINT Builder", "Prompt Preview", "Code Preview", "Chat Lab", "Version History", "Export"],
)

if "spec" not in st.session_state:
    st.session_state.spec = AgentSpec(
        agent_name="",
        use_case="",
        behaviour_values="",
        limitations_non_goals="",
        purpose="",
        parameters_configuration="",
        requirements="",
        version_notes="",
    )

if "builder_step" not in st.session_state:
    st.session_state.builder_step = 0

spec: AgentSpec = st.session_state.spec


def build_runtime_namespace(current_spec: AgentSpec) -> dict:
    """Render generated code and execute it in an isolated namespace."""
    generated_code = render_smolagents_code(current_spec, "Hugging Face")
    runtime_ns: dict = {}
    exec(generated_code, runtime_ns)
    return runtime_ns


def run_selected_tool(runtime_ns: dict, tool_name: str, user_prompt: str) -> str:
    agent = runtime_ns["build_sagemind_agent"]()
    if tool_name not in agent.tools:
        raise ValueError(f"Tool '{tool_name}' not found in generated runtime.")
    return str(agent.tools[tool_name].run(user_prompt))


def load_capability_demo() -> None:
    st.session_state.spec = AgentSpec(
        agent_name="SupportOps Copilot",
        use_case="Assist support teams by triaging customer issues, drafting responses, and routing urgent cases.",
        behaviour_values="Be empathetic, concise, and transparent about uncertainty.",
        limitations_non_goals="Cannot issue refunds directly, cannot access customer PII unless provided explicitly.",
        purpose="Reduce first response time and improve ticket quality.",
        parameters_configuration="Response style: concise. Escalate if payment/security/legal risk appears.",
        requirements="Use approved knowledge base and summarize citations in every answer.",
        version_notes="Demo preset for showcasing BLUEPRINT capabilities.",
        human_approval_rules="Require human approval before any billing or account-permission action.",
        memory_policy="Retain non-sensitive ticket context for 7 days; never store secrets.",
        memory_mode=MemoryMode.SESSION,
        interfaces_tools=[
            ToolSpec(
                name="search_kb",
                description="Search knowledge base articles",
                inputs="query: str",
                outputs="Top 3 relevant articles",
                function_body='return ["KB-102", "KB-212", "KB-998"]',
                permission_level=PermissionLevel.READ_ONLY,
            )
        ],
        examples=[
            TestCase(
                prompt="Customer says MFA codes fail after phone change.",
                expected="Ask verification steps, propose secure recovery flow, and escalate if lockout persists.",
                category="functional",
            )
        ],
    )


if page == "Home":
    st.markdown(
        """
        <div class="hero">
            <h3 style="margin: 0 0 0.35rem 0;">Design production-ready AI agents faster</h3>
            <p style="margin: 0; opacity: 0.95;">Build structured BLUEPRINT specs, test guardrails, generate prompts, and export runnable smolagents code from one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="capability-card"><strong>🧠 Structured design</strong><br/>Capture use-case, values, limits, and operational requirements.</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="capability-card"><strong>🛡️ Guardrails-first</strong><br/>Track approval rules, memory policy, and permissioned tools.</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="capability-card"><strong>⚙️ One-click outputs</strong><br/>Preview prompt + code and export artifacts for your runtime.</div>', unsafe_allow_html=True)

    st.subheader("Quick start")
    if st.button("Load capability demo"):
        load_capability_demo()
        st.success("Demo spec loaded. Open BLUEPRINT Builder, Prompt Preview, or Code Preview.")

elif page == "BLUEPRINT Builder":
    steps = [
        "Agent name",
        "Use case",
        "Behaviour & values",
        "Limitations & non-goals",
        "Purpose",
        "Parameters & configuration",
        "Requirements",
        "Version notes",
    ]

    st.subheader("Step-by-step builder")
    st.caption(f"Step {st.session_state.builder_step + 1} of {len(steps)}: {steps[st.session_state.builder_step]}")

    draft_names = list_drafts()
    selected_draft = st.selectbox("Load saved draft", ["(none)"] + draft_names)
    if st.button("Load selected draft") and selected_draft != "(none)":
        loaded = load_draft(selected_draft)
        if loaded:
            st.session_state.spec = loaded
            spec = st.session_state.spec
            st.success(f"Loaded draft: {selected_draft}")

    with st.form("step_form"):
        if st.session_state.builder_step == 0:
            spec.agent_name = st.text_input("Agent name", value=spec.agent_name)
        elif st.session_state.builder_step == 1:
            spec.use_case = st.text_area("Use case", value=spec.use_case)
        elif st.session_state.builder_step == 2:
            spec.behaviour_values = st.text_area("Behaviour & Values", value=spec.behaviour_values)
        elif st.session_state.builder_step == 3:
            spec.limitations_non_goals = st.text_area("Limitations & Non-Goals", value=spec.limitations_non_goals)
        elif st.session_state.builder_step == 4:
            spec.purpose = st.text_area("Purpose", value=spec.purpose)
        elif st.session_state.builder_step == 5:
            spec.parameters_configuration = st.text_area("Parameters & Configuration", value=spec.parameters_configuration)
        elif st.session_state.builder_step == 6:
            spec.requirements = st.text_area("Requirements", value=spec.requirements)
        elif st.session_state.builder_step == 7:
            spec.version_notes = st.text_area("Version notes", value=spec.version_notes)

        back = st.form_submit_button("⬅ Back")
        next_btn = st.form_submit_button("Next ➡")

    if back:
        st.session_state.builder_step = max(0, st.session_state.builder_step - 1)
        st.rerun()

    if next_btn:
        save_draft(spec)
        st.success("Draft saved.")
        st.session_state.builder_step = min(len(steps) - 1, st.session_state.builder_step + 1)
        st.rerun()

    st.divider()
    st.subheader("Advanced sections")
    spec.human_approval_rules = st.text_area("Human approval rules", value=spec.human_approval_rules)
    spec.memory_policy = st.text_area("Memory policy", value=spec.memory_policy)
    spec.memory_mode = MemoryMode(st.selectbox("Memory mode", [m.value for m in MemoryMode], index=[m.value for m in MemoryMode].index(spec.memory_mode.value)))

    st.subheader("Add tool")
    with st.form("tool_form"):
        t_name = st.text_input("Tool name")
        t_desc = st.text_input("Description")
        t_inputs = st.text_input("Inputs")
        t_outputs = st.text_input("Outputs")
        t_body = st.text_area("Python function body", value='return "tool output"')
        t_perm = st.selectbox("Permission", [p.value for p in PermissionLevel])
        add_tool = st.form_submit_button("Add tool")
    if add_tool and t_name:
        spec.interfaces_tools.append(
            ToolSpec(
                name=t_name,
                description=t_desc,
                inputs=t_inputs,
                outputs=t_outputs,
                function_body=t_body,
                permission_level=PermissionLevel(t_perm),
            )
        )
        save_draft(spec)
        st.success("Tool added and draft saved.")

elif page == "Prompt Preview":
    prompt = render_system_prompt(spec)
    st.code(prompt, language="markdown")

elif page == "Code Preview":
    backend = st.selectbox("Model backend", ["Hugging Face", "LiteLLM", "OpenAI-compatible", "Ollama"])
    code = render_smolagents_code(spec, backend)
    st.code(code, language="python")

elif page == "Chat Lab":
    st.subheader("Run generated agent/tool")
    st.caption("Execute the generated SageMind runtime from your current BLUEPRINT spec.")

    mode = st.radio("Mode", ["Agent", "Tool"], horizontal=True)
    user_prompt = st.text_area("Prompt", placeholder="Ask a question to run against your generated runtime")

    tool_name = None
    if mode == "Tool":
        tool_names = [tool.name for tool in spec.interfaces_tools]
        if tool_names:
            tool_name = st.selectbox("Choose tool", tool_names)
        else:
            st.warning("No tools configured yet. Add a tool in BLUEPRINT Builder first.")

    if st.button("Run"):
        if not user_prompt.strip():
            st.warning("Please provide a prompt.")
        else:
            try:
                runtime_ns = build_runtime_namespace(spec)
                with st.spinner("Running generated runtime..."):
                    if mode == "Agent":
                        runtime_agent = runtime_ns["build_sagemind_agent"]()
                        result = runtime_agent.run(user_prompt)
                    else:
                        if not tool_name:
                            st.stop()
                        result = run_selected_tool(runtime_ns, tool_name, user_prompt)

                st.write("**Response**")
                st.success(str(result))
            except Exception as exc:
                st.error(f"Runtime execution failed: {exc}")
                st.info("Tip: confirm your model credentials/environment for smolagents are configured.")

elif page == "Version History":
    st.write("Save current version")
    version = st.text_input("Version", value="0.1.0")
    author = st.text_input("Author", value="local-user")
    summary = st.text_area("Change summary")
    if st.button("Save version"):
        save_version(spec, version, author, summary)
        st.success("Version saved.")
    if spec.agent_name:
        st.table(list_versions(spec.agent_name))

elif page == "Export":
    prompt = render_system_prompt(spec)
    code = render_smolagents_code(spec, "Hugging Face")
    spec_json = spec.model_dump_json(indent=2)

    st.download_button("Download agent_spec.json", spec_json, file_name="agent_spec.json")
    st.download_button("Download system_prompt.md", prompt, file_name="system_prompt.md")
    st.download_button("Download smolagents_app.py", code, file_name="smolagents_app.py")

    if st.button("Write export files to ./exports"):
        out = Path("exports")
        out.mkdir(exist_ok=True)
        (out / "agent_spec.json").write_text(spec_json, encoding="utf-8")
        (out / "system_prompt.md").write_text(prompt, encoding="utf-8")
        (out / "smolagents_app.py").write_text(code, encoding="utf-8")
        st.success("Files exported to exports/.")
