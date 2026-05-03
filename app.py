from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from generators.prompt_generator import render_system_prompt
from generators.smolagents_generator import render_smolagents_code
from schemas.blueprint_schema import AgentSpec, MemoryMode, PermissionLevel, TestCase, ToolSpec
from storage.db import init_db, list_versions, save_version

init_db()
st.set_page_config(page_title="BLUEPRINT Agent Builder", layout="wide")
st.title("Streamlit BLUEPRINT Agent Builder (smolagents)")

st.sidebar.header("Project")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "BLUEPRINT Builder", "Prompt Preview", "Code Preview", "Test Lab", "Version History", "Export"],
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

spec: AgentSpec = st.session_state.spec

if page == "Home":
    st.write("Create or load an agent specification using BLUEPRINT sections.")

elif page == "BLUEPRINT Builder":
    with st.form("builder"):
        spec.agent_name = st.text_input("Agent name", value=spec.agent_name)
        spec.use_case = st.text_area("Use case", value=spec.use_case)
        spec.behaviour_values = st.text_area("Behaviour & Values", value=spec.behaviour_values)
        spec.limitations_non_goals = st.text_area("Limitations & Non-Goals", value=spec.limitations_non_goals)
        spec.purpose = st.text_area("Purpose", value=spec.purpose)
        spec.parameters_configuration = st.text_area("Parameters & Configuration", value=spec.parameters_configuration)
        spec.requirements = st.text_area("Requirements", value=spec.requirements)
        spec.version_notes = st.text_area("Version notes", value=spec.version_notes)
        spec.human_approval_rules = st.text_area("Human approval rules", value=spec.human_approval_rules)
        spec.memory_policy = st.text_area("Memory policy", value=spec.memory_policy)
        spec.memory_mode = MemoryMode(st.selectbox("Memory mode", [m.value for m in MemoryMode], index=0))
        submitted = st.form_submit_button("Save draft")

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

    st.subheader("Add example test")
    with st.form("example_form"):
        ex_prompt = st.text_input("Prompt")
        ex_expected = st.text_input("Expected response")
        ex_cat = st.selectbox("Category", ["functional", "guardrail", "tool"])
        add_example = st.form_submit_button("Add example")
    if add_example and ex_prompt:
        spec.examples.append(TestCase(prompt=ex_prompt, expected=ex_expected, category=ex_cat))

    st.write("### BLUEPRINT scorecard")
    checks = spec.to_scorecard()
    st.metric("Score", spec.blueprint_score())
    st.json(checks)

    if submitted:
        st.success("Draft saved in session.")

elif page == "Prompt Preview":
    prompt = render_system_prompt(spec)
    st.code(prompt, language="markdown")

elif page == "Code Preview":
    backend = st.selectbox("Model backend", ["Hugging Face", "LiteLLM", "OpenAI-compatible", "Ollama"])
    code = render_smolagents_code(spec, backend)
    st.code(code, language="python")

elif page == "Test Lab":
    st.write("MVP local test harness (simulated).")
    user_prompt = st.text_area("Single test prompt")
    if st.button("Run test") and user_prompt:
        st.write("**Agent answer**")
        st.info("Simulation only in MVP: connect runtime agent execution in V2.")
        st.write("**Pass/fail**: manual review required")

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
