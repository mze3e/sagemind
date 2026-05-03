from __future__ import annotations

from jinja2 import Environment, FileSystemLoader

from schemas.blueprint_schema import AgentSpec


def render_smolagents_code(spec: AgentSpec, model_backend: str, template_dir: str = "templates") -> str:
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("smolagent_code.jinja")
    return template.render(spec=spec, model_backend=model_backend)
