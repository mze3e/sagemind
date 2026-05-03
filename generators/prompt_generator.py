from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from schemas.blueprint_schema import AgentSpec


def render_system_prompt(spec: AgentSpec, template_dir: str = "templates") -> str:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(disabled_extensions=("jinja",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("system_prompt.jinja")
    return template.render(spec=spec)


def save_system_prompt(prompt: str, output_path: str | Path) -> None:
    Path(output_path).write_text(prompt, encoding="utf-8")
