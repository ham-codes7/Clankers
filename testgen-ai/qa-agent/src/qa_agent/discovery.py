
import os
import re
from rich.console import Console
from rich.table import Table


class ProjectDiscovery:
    """Discover various components within the project directory.

    This class scans the project's working directory to identify OpenAPI specifications,
    Python source files, Playwright trace files, and detect the web framework in use.
    """

    def __init__(self, root_path: str = "."):
        """Initializes the ProjectDiscovery with a root path.

        Args:
            root_path (str): The root directory to start scanning from. Defaults to ".".
        """
        self.root_path = root_path
        self.console = Console()
        self.console.print(f"[Discovery] Scanning project at {os.path.abspath(root_path)}...")

    def find_openapi_specs(self) -> list[str]:
        """Finds OpenAPI specification files within the project.

        It looks for files named 'openapi.yaml', 'openapi.json', 'swagger.yaml', 'swagger.json',
        and any .yaml or .json file containing 'openapi:' in its first 5 lines.

        Returns:
            list[str]: A list of paths to the discovered OpenAPI specification files.
        """
        openapi_specs = []
        # Walk through the directory recursively
        for dirpath, _, filenames in os.walk(self.root_path):
            for filename in filenames:
                # Check for standard OpenAPI filenames
                if filename in ["openapi.yaml", "openapi.json", "swagger.yaml", "swagger.json"]:
                    openapi_specs.append(os.path.join(dirpath, filename))
                    continue

                # Check for files containing "openapi:" in the first 5 lines
                if filename.endswith((".yaml", ".json")):
                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            # Read first 5 lines to check for 'openapi:' keyword
                            for i, line in enumerate(f):
                                if i >= 5:
                                    break
                                if "openapi:" in line:
                                    openapi_specs.append(filepath)
                                    break
                    except Exception as e:
                        self.console.print(f"[Discovery] Error reading {filepath}: {e}")

        self.console.print(f"[Discovery] Found {len(openapi_specs)} OpenAPI specs")
        return openapi_specs

    def find_python_source(self) -> list[str]:
        """Finds Python source (.py) files within the project.

        Excludes common non-source directories like __pycache__, venv, .venv, tests/, and migrations/.

        Returns:
            list[str]: A list of paths to the discovered Python source files.
        """
        python_files = []
        exclude_dirs = ["__pycache__", "venv", ".venv", "tests", "migrations"]
        # Walk through the directory recursively
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            # Modify dirnames in-place to exclude directories from future walks
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

            for filename in filenames:
                # Check for Python files
                if filename.endswith(".py"):
                    python_files.append(os.path.join(dirpath, filename))

        self.console.print(f"[Discovery] Found {len(python_files)} Python source files")
        return python_files

    def find_playwright_traces(self) -> list[str]:
        """Finds Playwright trace files (zip files containing 'trace') within the project.

        Returns:
            list[str]: A list of paths to the discovered Playwright trace files.
        """
        playwright_traces = []
        # Walk through the directory recursively
        for dirpath, _, filenames in os.walk(self.root_path):
            for filename in filenames:
                # Check for zip files with 'trace' in their name
                if filename.endswith(".zip") and "trace" in filename.lower():
                    playwright_traces.append(os.path.join(dirpath, filename))

        self.console.print(f"[Discovery] Found {len(playwright_traces)} Playwright traces")
        return playwright_traces

    def detect_framework(self) -> str:
        """Detects the web framework used in the project.

        It checks `requirements.txt` and `pyproject.toml` for common framework dependencies.

        Returns:
            str: The detected framework (e.g., "fastapi", "flask", "django") or "unknown".
        """
        framework = "unknown"
        # List of framework dependencies to check
        framework_dependencies = {
            "fastapi": "fastapi",
            "flask": "flask",
            "django": "django",
        }

        # Check requirements.txt
        requirements_path = os.path.join(self.root_path, "requirements.txt")
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for fw, dep in framework_dependencies.items():
                        if re.search(r"^" + re.escape(dep) + r"[=~<>!]*", content, re.MULTILINE):
                            framework = fw
                            break
            except Exception as e:
                self.console.print(f"[Discovery] Error reading {requirements_path}: {e}")

        # If not found, check pyproject.toml
        if framework == "unknown":
            pyproject_path = os.path.join(self.root_path, "pyproject.toml")
            if os.path.exists(pyproject_path):
                try:
                    with open(pyproject_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for fw, dep in framework_dependencies.items():
                            # Search within the [project.dependencies] section
                            if re.search(r"\[project\.dependencies\].*?\n[^\n]*?" + re.escape(dep) + r"[=~<>!]*", content, re.DOTALL):
                                framework = fw
                                break
                except Exception as e:
                    self.console.print(f"[Discovery] Error reading {pyproject_path}: {e}")

        self.console.print(f"[Discovery] Detected framework: {framework}")
        return framework

    def run(self) -> dict:
        """Executes all discovery methods and returns a summary.

        Returns:
            dict: A dictionary containing the discovered OpenAPI specs, Python files,
                  Playwright traces, and the detected framework.
        """
        openapi_specs = self.find_openapi_specs()
        python_files = self.find_python_source()
        playwright_traces = self.find_playwright_traces()
        framework = self.detect_framework()

        summary = {
            "openapi_specs": openapi_specs,
            "python_files": python_files,
            "playwright_traces": playwright_traces,
            "framework": framework,
        }

        self.console.print("\n[Discovery Summary]")
        table = Table(title="Project Discovery Results")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Count", style="magenta")
        table.add_column("Details", style="green")

        table.add_row("OpenAPI Specs", str(len(openapi_specs)), "\n".join(openapi_specs) if openapi_specs else "None")
        table.add_row("Python Source Files", str(len(python_files)), "\n".join(python_files) if python_files else "None")
        table.add_row("Playwright Traces", str(len(playwright_traces)), "\n".join(playwright_traces) if playwright_traces else "None")
        table.add_row("Detected Framework", "N/A", framework)

        self.console.print(table)

        return summary


if __name__ == "__main__":
    # Example of how to use the ProjectDiscovery class
    # This block only runs when the script is executed directly
    discovery = ProjectDiscovery("testgen-ai/qa-agent/")
    results = discovery.run()
    print("\nRaw Results:", results)
