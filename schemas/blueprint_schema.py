from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PermissionLevel(str, Enum):
    READ_ONLY = "read_only"
    WRITE = "write"
    APPROVAL_REQUIRED = "approval_required"


class MemoryMode(str, Enum):
    NONE = "none"
    SESSION = "session"
    SUMMARY = "summary"
    PERSISTENT = "persistent"


class ToolSpec(BaseModel):
    name: str
    description: str
    inputs: str
    outputs: str
    function_body: str
    permission_level: PermissionLevel = PermissionLevel.READ_ONLY


class TestCase(BaseModel):
    prompt: str
    expected: str
    category: str = "functional"


class VersionEntry(BaseModel):
    version: str
    author: str
    change_summary: str
    blueprint_score: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentSpec(BaseModel):
    agent_name: str
    use_case: str
    behaviour_values: str
    limitations_non_goals: str
    purpose: str
    examples: List[TestCase] = Field(default_factory=list)
    parameters_configuration: str
    requirements: str
    interfaces_tools: List[ToolSpec] = Field(default_factory=list)
    version_notes: str
    memory_mode: MemoryMode = MemoryMode.NONE
    memory_policy: str = "Do not store sensitive data unless explicitly enabled."
    human_approval_rules: str = "Require approval for write actions."
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_scorecard(self) -> dict[str, bool]:
        return {
            "persona": bool(self.behaviour_values.strip()),
            "non_goals": bool(self.limitations_non_goals.strip()),
            "input_output_format": bool(self.parameters_configuration.strip()),
            "tool_permissions": all(t.permission_level for t in self.interfaces_tools) or not self.interfaces_tools,
            "human_approval_rules": bool(self.human_approval_rules.strip()),
            "test_cases": len(self.examples) > 0,
            "memory_policy": bool(self.memory_policy.strip()),
            "version_notes": bool(self.version_notes.strip()),
        }

    def blueprint_score(self) -> int:
        checks = self.to_scorecard()
        return int((sum(checks.values()) / len(checks)) * 100)
