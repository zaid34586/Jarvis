# -*- coding: utf-8 -*-

def build_custom_prompt(task_type: str, user_requirement: str) -> str:
    """Generates highly structured, targeted system prompts for sub-tasks."""
    base_prompt = f"""[SYSTEM ROLE: SPECIALIZED {task_type.upper()} AGENT]
CONTEXT & GOAL:
{user_requirement}

EXECUTION RULES:
1. Provide production-ready, highly efficient, modular code or operational steps.
2. Include error handling, safety checks, and edge-case validations.
3. Keep explanation concise, structured, and focused on immediate deployment.

OUTPUT FORMAT:
- Executive Summary (1-2 lines)
- Structured Code / Configuration
- Terminal / Execution Commands
"""
    return base_prompt
