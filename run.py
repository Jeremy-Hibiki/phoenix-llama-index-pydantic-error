#!/usr/bin/env python3
from __future__ import annotations

from enum import Enum

import rich
import typer
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register
from rich.prompt import Prompt


class ProviderType(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    VLLM = "vllm"


def setup():
    register(project_name="phoenix-llama-index-pydantic-error", endpoint="https://app.phoenix.arize.com/v1/traces")
    LlamaIndexInstrumentor().instrument()


def main(provider: ProviderType | None = None):
    setup()

    DEFAULT_API_URL = ""
    if provider == ProviderType.OPENAI:
        DEFAULT_API_URL = "https://api.openai.com/v1"
    elif provider == ProviderType.OLLAMA:
        DEFAULT_API_URL = "http://localhost:11434/v1"
    elif provider == ProviderType.VLLM:
        DEFAULT_API_URL = "http://localhost:8000/v1"

    DEFAULT_MODEL = ""
    if provider == ProviderType.OPENAI:
        DEFAULT_MODEL = "gpt-4o-mini"
    elif provider == ProviderType.OLLAMA:
        DEFAULT_MODEL = "qwen2:0.5b"
    elif provider == ProviderType.VLLM:
        DEFAULT_MODEL = "Qwen/Qwen2-0.5B-Instruct"

    DEFAULT_API_KEY = ""
    if provider == ProviderType.OLLAMA or provider == ProviderType.VLLM:
        DEFAULT_API_KEY = "EMPTY"

    api_url = Prompt.ask("API URL", default=DEFAULT_API_URL) or None
    api_key = Prompt.ask("API Key", default=DEFAULT_API_KEY, password=True) or None
    model = Prompt.ask("Model", default=DEFAULT_MODEL)

    if provider == ProviderType.OPENAI:
        llm = OpenAI(model=model, api_key=api_key, api_base=api_url)
    else:
        llm = OpenAILike(
            model=model,
            api_key=api_key,
            api_base=api_url,
            max_tokens=64,
            context_window=32768,
            is_chat_model=True,
        )

    response = llm.chat(messages=[ChatMessage(content="Who are you?")])
    rich.print(response)


if __name__ == "__main__":
    typer.run(main)
