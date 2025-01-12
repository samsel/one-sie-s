# ai-browser-use

Take the help of an LLM and control your browser. In this example we will use a locally installed LLM.

## Install

Make sure ollama & playwright are installed in your local machine and a model like llama3.1 is downloaded.

```bash
pip install browser-use
uv venv --python 3.11
uv pip install -r requirements.txt
uv run agent.py
```