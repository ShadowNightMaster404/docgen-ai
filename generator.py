import httpx
from parser import CodeParser, FunctionInfo


class DocstringGenerator:
    """Generates docstrings using local LLM via Ollama."""
    
    def __init__(self, model: str = "llama3.1:8b"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
    
    def generate_docstring(self, func: FunctionInfo) -> str:
        """Generate a docstring for a single function."""
        
        prompt = self._build_prompt(func)
        
        response = httpx.post(
            self.ollama_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,  # Low = more deterministic
                    "num_predict": 256   # Limit output length
                }
            },
            timeout=60.0
        )
        
        return self._clean_response(response.json()["response"])
    
    def _build_prompt(self, func: FunctionInfo) -> str:
        """Build a focused prompt for docstring generation."""
        
        return f'''Write a Python docstring for this function. Return ONLY the docstring content, no quotes, no code.

Function name: {func.name}
Arguments: {", ".join(func.args) if func.args else "none"}
Code:
{func.body_preview}

Write a clear, concise docstring that describes:
1. What the function does (one sentence)
2. Args: each parameter and its purpose
3. Returns: what the function returns

Docstring:'''
    
    def _clean_response(self, response: str) -> str:
        """Clean up LLM response to get just the docstring."""
        # Remove common artifacts
        response = response.strip()
        response = response.strip('"""').strip("'''")
        return response


# Test it
if __name__ == "__main__":
    test_code = '''
def calculate_total(items, tax_rate):
    subtotal = sum(item.price for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax
'''
    
    parser = CodeParser(test_code)
    functions = parser.extract_functions()
    generator = DocstringGenerator()
    
    for func in functions:
        if not func.has_docstring:
            print(f"Generating docstring for: {func.name}")
            docstring = generator.generate_docstring(func)
            print(f"Result:\n{docstring}\n")