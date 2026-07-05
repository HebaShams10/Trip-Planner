from dataclasses import dataclass
from ChatBot.shortcuts import SHORTCUT_REGISTRY
from ChatBot import config

@dataclass
class ResolvedInput:
    prompt: str
    shortcut_used: str = None
    temperature: float = config.temperature
    max_tokens: int = config.max_tokens

def resolve_shortcut(raw_input: str):
    for trigger, definition in SHORTCUT_REGISTRY.items():
        if raw_input.strip().startswith(trigger):
            suffix = raw_input[len(trigger):].strip()
            return ResolvedInput(
                prompt=definition.expansion + suffix,
                shortcut_used=trigger,
                temperature=definition.temperature,
                max_tokens=definition.max_tokens
            )
    return ResolvedInput(prompt=raw_input)