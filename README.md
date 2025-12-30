\# DocGen AI



Generate Python docstrings automatically using a local LLM.



!\[Python](https://img.shields.io/badge/Python-3.10+-blue)

!\[License](https://img.shields.io/badge/License-MIT-green)

!\[Local](https://img.shields.io/badge/Runs-100%25%20Local-orange)



\## Why?



Developers skip documentation because it's tedious. This tool reads your code and writes clear docstrings in seconds — completely offline, no API costs.



\## Features



\- \*\*100% Local\*\* — Runs on your machine using LLaMA 3.1 8B via Ollama

\- \*\*Smart Parsing\*\* — Uses Python AST to extract functions accurately

\- \*\*Handles Everything\*\* — Regular functions, class methods, async functions

\- \*\*Skip Existing\*\* — Won't overwrite functions that already have docstrings

\- \*\*Easy Interface\*\* — Paste code or upload .py files



\## Demo



Paste this:

```python

def calculate\_total(items, tax\_rate):

&nbsp;   subtotal = sum(item.price for item in items)

&nbsp;   return subtotal + (subtotal \* tax\_rate)

```



Get this:

```python

def calculate\_total(items, tax\_rate):

&nbsp;   """

&nbsp;   Calculate the total price including tax.

&nbsp;   

&nbsp;   Args:

&nbsp;       items: List of items with price attribute.

&nbsp;       tax\_rate: Tax rate as decimal (e.g., 0.08 for 8%).

&nbsp;   

&nbsp;   Returns:

&nbsp;       Total price with tax included.

&nbsp;   """

&nbsp;   subtotal = sum(item.price for item in items)

&nbsp;   return subtotal + (subtotal \* tax\_rate)

```



\## Tech Stack



\- \*\*LLaMA 3.1 8B\*\* — Quantized model runs on 6GB VRAM

\- \*\*Ollama\*\* — Local LLM inference server

\- \*\*FastAPI\*\* — Python web framework

\- \*\*Python AST\*\* — Code parsing and analysis



\## Requirements



\- Python 3.10+

\- Ollama installed

\- 6GB+ VRAM (or CPU fallback)



\## Installation



1\. Install Ollama: https://ollama.com/download



2\. Pull the model:

```bash

ollama pull llama3.1:8b

```



3\. Clone and setup:

```bash

git clone https://github.com/YOUR\_USERNAME/docgen-ai.git

cd docgen-ai

python -m venv venv

venv\\Scripts\\activate  # Windows

pip install -r requirements.txt

```



4\. Run:

```bash

python main.py

```



5\. Open http://127.0.0.1:8000



\## Project Structure

```

docgen-ai/

├── main.py          # FastAPI web server

├── parser.py        # AST code parser

├── generator.py     # LLM docstring generator

├── requirements.txt

└── README.md

```



\## How It Works



1\. \*\*Parse\*\* — AST extracts function signatures and code bodies

2\. \*\*Filter\*\* — Skip functions that already have docstrings

3\. \*\*Generate\*\* — LLM writes docstrings from focused prompts

4\. \*\*Insert\*\* — Docstrings placed back into original code



\## License



MIT

