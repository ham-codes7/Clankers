# Purpose: This utility will handle parsing various input file types (e.g., Python, JavaScript) to extract relevant code for test generation.

import re
import json
import yaml

def parse_uploaded_file(file_content: str, file_type: str) -> dict:
    """
    Parses the content of an uploaded file based on its type and extracts relevant information.
    Returns a dictionary with language, content, extracted functions/keys, line count, and a summary.
    """
    print(f"Parsing file of type: {file_type}")

    # Initialize default values for the result dictionary
    result = {
        "language": "unknown",
        "content": file_content,
        "functions": [],
        "line_count": len(file_content.splitlines()),
        "summary": ""
    }

    # --- Python File Parsing ---
    # Detects and parses Python files.
    if file_type == ".py":
        print("Detected Python file. Extracting function names.")
        result["language"] = "python"
        result["summary"] = "Python source code file"
        # Regex to find function definitions: 'def function_name(' optionally followed by spaces
        function_names = re.findall(r"^\s*def\s+(\w+)\(.*?\):", file_content, re.MULTILINE)
        result["functions"] = function_names

    # --- JavaScript/TypeScript File Parsing ---
    # Detects and parses JavaScript/TypeScript files.
    elif file_type in [".js", ".ts"]:
        print(f"Detected {file_type} file. Extracting function/const names.")
        result["language"] = "javascript" if file_type == ".js" else "typescript"
        result["summary"] = f"{file_type} source code file"
        # Regex to find function declarations (function name) or arrow function expressions (const name = () =>)
        # This regex covers 'function myFunction(' and 'const myFunction = ('
        function_names = re.findall(r"(?:^|\s)(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:function)?\s*\(.*?\)\s*=>)", file_content, re.MULTILINE)
        # Flatten the list of tuples and remove None values
        clean_function_names = [name for tpl in function_names for name in tpl if name]
        result["functions"] = clean_function_names

    # --- YAML File Parsing ---
    # Detects and parses YAML files, extracting top-level keys.
    elif file_type in [".yaml", ".yml"]:
        print("Detected YAML file. Extracting top-level keys.")
        result["language"] = "yaml"
        result["summary"] = "YAML configuration or data file"
        try:
            # Load YAML content
            yaml_content = yaml.safe_load(file_content)
            if isinstance(yaml_content, dict):
                result["functions"] = list(yaml_content.keys())
        except yaml.YAMLError as e:
            print(f"Error parsing YAML content: {e}")
            result["summary"] = "YAML file with parsing errors"

    # --- JSON File Parsing ---
    # Detects and parses JSON files, extracting top-level keys.
    elif file_type == ".json":
        print("Detected JSON file. Extracting top-level keys.")
        result["language"] = "json"
        result["summary"] = "JSON data file"
        try:
            # Load JSON content
            json_content = json.loads(file_content)
            if isinstance(json_content, dict):
                result["functions"] = list(json_content.keys())
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON content: {e}")
            result["summary"] = "JSON file with parsing errors"

    # --- Text File Parsing ---
    # Handles plain text files, returning content as-is.
    elif file_type == ".txt":
        print("Detected plain text file. No specific extraction.")
        result["language"] = "text"
        result["summary"] = "Plain text file"
        # No function/key extraction for text files

    # --- Unsupported File Type ---
    # Catches any file types not explicitly supported.
    else:
        print("Unsupported file type.")
        result["summary"] = "Unsupported file type"

    print("File parsing complete.")
    return result

if __name__ == "__main__":
    # Sample Python code for testing
    sample_python_code = """
import os

def calculate_sum(a, b):
    # Calculates the sum of two numbers
    return a + b

class MyClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

async def fetch_data(url):
    # Fetches data from a URL asynchronously
    pass
"""

    print("\n--- Testing Python File ---")
    python_parsed = parse_uploaded_file(sample_python_code, ".py")
    print("Parsed Python Data:", python_parsed)
    assert python_parsed["language"] == "python"
    assert "calculate_sum" in python_parsed["functions"]
    assert "get_value" in python_parsed["functions"]
    assert "fetch_data" in python_parsed["functions"]
    assert python_parsed["line_count"] == 13
    assert python_parsed["summary"] == "Python source code file"

    # Sample JavaScript code for testing
    sample_js_code = """
function greet(name) {
    return `Hello, ${name}`;
}

const add = (a, b) => a + b;

class Calculator {
    constructor() {
        this.result = 0;
    }

    multiply(a, b) {
        return a * b;
    }
}
"""
    print("\n--- Testing JavaScript File ---")
    js_parsed = parse_uploaded_file(sample_js_code, ".js")
    print("Parsed JavaScript Data:", js_parsed)
    assert js_parsed["language"] == "javascript"
    assert "greet" in js_parsed["functions"]
    assert "add" in js_parsed["functions"]
    assert "multiply" in js_parsed["functions"]
    assert js_parsed["line_count"] == 14
    assert js_parsed["summary"] == ".js source code file"

    # Sample YAML content for testing
    sample_yaml_content = """
app:
  name: TestGen AI
  version: 1.0.0
database:
  host: localhost
  port: 5432
"""
    print("\n--- Testing YAML File ---")
    yaml_parsed = parse_uploaded_file(sample_yaml_content, ".yaml")
    print("Parsed YAML Data:", yaml_parsed)
    assert yaml_parsed["language"] == "yaml"
    assert "app" in yaml_parsed["functions"]
    assert "database" in yaml_parsed["functions"]
    assert yaml_parsed["line_count"] == 6
    assert yaml_parsed["summary"] == "YAML configuration or data file"

    # Sample JSON content for testing
    sample_json_content = """
{
  "user": {
    "name": "Alice",
    "age": 30
  },
  "products": [
    {"id": 1, "name": "Laptop"}
  ]
}
"""
    print("\n--- Testing JSON File ---")
    json_parsed = parse_uploaded_file(sample_json_content, ".json")
    print("Parsed JSON Data:", json_parsed)
    assert json_parsed["language"] == "json"
    assert "user" in json_parsed["functions"]
    assert "products" in json_parsed["functions"]
    assert json_parsed["line_count"] == 9
    assert json_parsed["summary"] == "JSON data file"

    # Sample text content for testing
    sample_text_content = """
This is a plain text file.
It has multiple lines.
No special parsing should happen here.
"""
    print("\n--- Testing Text File ---")
    text_parsed = parse_uploaded_file(sample_text_content, ".txt")
    print("Parsed Text Data:", text_parsed)
    assert text_parsed["language"] == "text"
    assert text_parsed["functions"] == []
    assert text_parsed["line_count"] == 3
    assert text_parsed["summary"] == "Plain text file"

    print("\nAll assertions passed! File parser is working as expected.")
