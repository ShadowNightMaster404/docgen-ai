\# DocGen AI



Generate Python docstrings automatically using a local LLM.



\## Why?



Developers skip documentation because it's tedious. This tool reads your code and writes clear docstrings in seconds - completely offline, no API costs.



\## Features



\- 100% Local - Runs on your machine using LLaMA 3.1 8B via Ollama

\- Smart Parsing - Uses Python AST to extract functions accurately

\- Handles Everything - Regular functions, class methods, async functions

\- Skip Existing - Won't overwrite functions that already have docstrings

\- Easy Interface - Paste code or upload .py files



\## Demo



Paste this:



def calculate\_total(items, tax\_rate):

&nbsp;   subtotal = sum(item.price for item in items)

&nbsp;   return subtotal + (subtotal \* tax\_rate)



Get this:



def calculate\_total(items, tax\_rate):

&nbsp;   """

&nbsp;   Calculate the total price including tax.

&nbsp;   

&nbsp;   Args:

&nbsp;       items: List of items with price attribute.

&nbsp;       tax\_rate: Tax rate as decimal.

&nbsp;   

&nbsp;   Returns:

&nbsp;       Total price with tax included.

&nbsp;   """

&nbsp;   subtotal = sum(item.price for item in items)

&nbsp;   return subtotal + (subtotal \* tax\_rate)



\## Tech Stack



\- LLaMA 3.1 8B - Quantized model runs on 6GB VRAM

\- Ollama - Local LLM inference server

\- FastAPI - Python web framework

\- Python AST - Code parsing and analysis



\## Requirements



\- Python 3.10+

\- Ollama installed

\- 6GB+ VRAM (or CPU fallback)



\## Installation



1\. Install Ollama from https://ollama.com/download



2\. Pull the model:



ollama pull llama3.1:8b



3\. Clone and setup:



git clone https://github.com/ShadowNightMaster404/docgen-ai.git

cd docgen-ai

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



4\. Run:



python main.py



5\. Open http://127.0.0.1:8000



\## License



MIT

