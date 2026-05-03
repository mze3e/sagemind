from __future__ import annotations

from schemas.blueprint_schema import ToolSpec


def generate_tool_function(tool: ToolSpec) -> str:
    return f'''@tool\ndef {tool.name}(input_text: str) -> str:\n    """{tool.description}\n\n    Permission: {tool.permission_level.value}\n    Inputs: {tool.inputs}\n    Outputs: {tool.outputs}\n    """\n{indent_block(tool.function_body, 1)}\n'''


def indent_block(text: str, level: int) -> str:
    prefix = "    " * level
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())
