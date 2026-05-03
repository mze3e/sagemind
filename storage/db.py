from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from schemas.blueprint_schema import AgentSpec

DB_PATH = Path("storage/blueprint_agents.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                version TEXT NOT NULL,
                author TEXT NOT NULL,
                change_summary TEXT,
                blueprint_score INTEGER,
                spec_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL UNIQUE,
                spec_json TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_version(spec: AgentSpec, version: str, author: str, change_summary: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO agent_versions (agent_name, version, author, change_summary, blueprint_score, spec_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                spec.agent_name,
                version,
                author,
                change_summary,
                spec.blueprint_score(),
                spec.model_dump_json(indent=2),
            ),
        )


def list_versions(agent_name: str) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT version, author, change_summary, blueprint_score, created_at
            FROM agent_versions
            WHERE agent_name = ?
            ORDER BY id DESC
            """,
            (agent_name,),
        ).fetchall()
    return [
        {
            "version": r[0],
            "author": r[1],
            "change_summary": r[2],
            "blueprint_score": r[3],
            "created_at": r[4],
        }
        for r in rows
    ]


def load_latest_spec(agent_name: str) -> AgentSpec | None:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT spec_json FROM agent_versions WHERE agent_name = ? ORDER BY id DESC LIMIT 1",
            (agent_name,),
        ).fetchone()
    if not row:
        return None
    data = json.loads(row[0])
    return AgentSpec.model_validate(data)


def save_draft(spec: AgentSpec) -> None:
    agent_name = spec.agent_name.strip() or "untitled-agent"
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO agent_drafts (agent_name, spec_json, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(agent_name)
            DO UPDATE SET spec_json = excluded.spec_json, updated_at = CURRENT_TIMESTAMP
            """,
            (agent_name, spec.model_dump_json(indent=2)),
        )


def load_draft(agent_name: str) -> AgentSpec | None:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT spec_json FROM agent_drafts WHERE agent_name = ?",
            (agent_name,),
        ).fetchone()
    if not row:
        return None
    return AgentSpec.model_validate(json.loads(row[0]))


def list_drafts() -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT agent_name FROM agent_drafts ORDER BY updated_at DESC").fetchall()
    return [r[0] for r in rows]
