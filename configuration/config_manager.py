# config_manager.py
import json
from typing import Dict, Any
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
class LLMFactory:
    _config = None

    @staticmethod
    def _load_config() -> Dict[str, Any]:
        if LLMFactory._config is None:
            config_path = Path(__file__).parent / "llm_config.json"
            with open(config_path) as f:
                LLMFactory._config = json.load(f)
        return LLMFactory._config

    @staticmethod
    def _get_framework() -> str:
        return LLMFactory._load_config()["llm"]["framework"].lower()

    @staticmethod
    def _get_model_config() -> Dict[str, Any]:
        config = LLMFactory._load_config()
        framework = LLMFactory._get_framework()
        model = config["llm"][framework]["model"]
        return {
            "MODEL": model,
            **config["llm"][framework]["model_kwargs"][model]
        }

    @staticmethod
    def get_llm():
        framework = LLMFactory._get_framework()
        config = LLMFactory._get_model_config()
        
        match framework:
            case 'openai':
                return ChatOpenAI(
                    model=config["MODEL"],
                    temperature=config.get("temperature"),
                    api_key=LLMFactory._load_config().get("api_keys", {}).get("openai") or None
                )
            case 'together':
                return ChatTogether(
                    model=config["MODEL"],
                    temperature=config.get("temperature"),
                    api_key=LLMFactory._load_config().get("api_keys", {}).get("together") or None
                )
            case 'anthropic':
                return ChatAnthropic(
                    model=config["MODEL"],
                    temperature=config.get("temperature"),
                    api_key=LLMFactory._load_config().get("api_keys", {}).get("anthropic") or None
                )
            case 'groq':
                return ChatGroq(
                    model=config["MODEL"],
                    temperature=config.get("temperature"),
                    api_key=LLMFactory._load_config().get("api_keys", {}).get("groq") or None
                )
            case _:
                raise ValueError(f"Unsupported framework: {framework}")