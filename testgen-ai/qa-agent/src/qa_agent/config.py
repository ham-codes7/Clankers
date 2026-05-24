
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .qa-agent.yaml.

    Settings are loaded in the following priority:
    1. Environment variables
    2. .qa-agent.yaml file in the current working directory
    """

    # Anthropic API key for accessing Claude models
    anthropic_api_key: str
    # Google Gemini API key for accessing Gemini models
    gemini_api_key: str

    # Default model to use for less 'deep' AI tasks
    model: str = "claude-sonnet-4-6"
    # Model to use for more 'deep' or complex AI tasks
    deep_model: str = "claude-opus-4-7"

    # Base URL for the application's backend API, useful for local development or testing
    base_url: str = "http://localhost:8000"
    # Directory where generated test files will be saved
    output_dir: str = "tests/generated"

    # Flag to enable or disable the use of 'deep' models for more complex tasks
    use_deep: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False, yaml_file=".qa-agent.yaml", yaml_file_kwargs={"encoding": "utf-8"})

def load_config() -> Settings:
    """Loads and returns the application settings.

    Handles missing API keys by raising a ValueError with a helpful message.
    """
    try:
        settings = Settings()
        if not settings.anthropic_api_key:
            raise ValueError(
                """ANTHROPIC_API_KEY not found. Please set the ANTHROPIC_API_KEY environment variable 
                or add it to a .qa-agent.yaml file."""
            )
        if not settings.gemini_api_key:
            raise ValueError(
                """GEMINI_API_KEY not found. Please set the GEMINI_API_KEY environment variable 
                or add it to a .qa-agent.yaml file."""
            )
        return settings
    except Exception as e:
        # Catch any other exceptions during settings loading and provide a generic error
        raise ValueError(f"Failed to load configuration: {e}")
