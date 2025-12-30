import ast
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    """Stores extracted information about a Python function."""
    name: str
    args: list[str]
    body_preview: str
    start_line: int
    end_line: int
    has_docstring: bool
    existing_docstring: str | None = None


class CodeParser:
    """
    Extracts function information from Python source code using AST.
    """
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.tree = ast.parse(source_code)
    
    def extract_functions(self) -> list[FunctionInfo]:
        """Walk the AST and extract all function definitions."""
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(self._process_function(node))
        return functions
    
    def _process_function(self, node) -> FunctionInfo:
        """Extract details from a single function node."""
        args = [arg.arg for arg in node.args.args]
        existing_docstring = ast.get_docstring(node)
        has_docstring = existing_docstring is not None
        
        body_start = node.body[0].lineno - 1
        if has_docstring and len(node.body) > 1:
            body_start = node.body[1].lineno - 1
        body_preview = "\n".join(self.lines[body_start:body_start + 5])
        
        return FunctionInfo(
            name=node.name,
            args=args,
            body_preview=body_preview,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            has_docstring=has_docstring,
            existing_docstring=existing_docstring
        )
    
    def insert_docstrings(self, docstrings: dict[str, str]) -> str:
        """
        Insert generated docstrings into the original code.
        
        Args:
            docstrings: Dict mapping function names to their new docstrings.
        
        Returns:
            Modified source code with docstrings inserted.
        """
        lines = self.source_code.splitlines()
        functions = sorted(self.extract_functions(), key=lambda f: f.start_line, reverse=True)
        
        for func in functions:
            if func.name in docstrings and not func.has_docstring:
                insert_line = func.start_line
                body_line = lines[insert_line] if insert_line < len(lines) else ""
                indent = len(body_line) - len(body_line.lstrip())
                if indent == 0:
                    indent = 4
                
                docstring_text = docstrings[func.name]
                formatted = self._format_docstring(docstring_text, indent)
                lines.insert(insert_line, formatted)
        
        return "\n".join(lines)
    
    def _format_docstring(self, docstring: str, indent: int) -> str:
        """Format a docstring with proper indentation and quotes."""
        spaces = " " * indent
        doc_lines = docstring.strip().splitlines()
        
        if len(doc_lines) == 1:
            return f'{spaces}"""{doc_lines[0]}"""'
        
        result = f'{spaces}"""\n'
        for line in doc_lines:
            if line.strip():
                result += f"{spaces}{line}\n"
            else:
                result += "\n"
        result += f'{spaces}"""'
        return result


if __name__ == "__main__":
    test_code = '''
def calculate_total(items, tax_rate):
    subtotal = sum(item.price for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax

def validate_email(email):
    """Check if email format is valid."""
    import re
    pattern = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
    return bool(re.match(pattern, email))
'''
    
    parser = CodeParser(test_code)
    functions = parser.extract_functions()
    
    for func in functions:
        print(f"Function: {func.name}, Has docstring: {func.has_docstring}")
