## Setup tracing

```bash
export OTEL_EXPORTER_OTLP_HEADERS="api_key=xxxxxxxxxxxxxxxxxxxxxxxxxx"
export PHOENIX_CLIENT_HEADERS="api_key=xxxxxxxxxxxxxxxxxxxxxxxxxx"
export PHOENIX_COLLECTOR_ENDPOINT="https://app.phoenix.arize.com"
```

## With OpenAI

```bash
python ./run.py --provider openai
```

Leave the API Key empty to read from environment.

Change the host and model name if needed.

## With Ollama

1. start a model service (refer to official document)

e.g. 0.5B Qwen2 model with Q4_0 (around 350MB to download)

```bash
ollama run qwen2:0.5b
```

2. run the python script

```bash
python ./run.py --provider ollama
```

## With vLLM

1. start a model service (refer to official document)

e.g. 0.5B Qwen2 model with AWQ (around 700MB to download)

```bash
vllm serve Qwen/Qwen2-0.5B-Instruct-AWQ --served_model_name=Qwen/Qwen2-0.5B-Instruct
```

2. run the python script

```bash
python ./run.py --provider vllm
```
