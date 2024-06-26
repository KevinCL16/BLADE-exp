import os
import os.path as osp
from dotenv import load_dotenv
from typing import Union
import hydra
from hydra import compose, initialize
import yaml


from blade_bench.llms.datamodel import TextGenConfig
from blade_bench.logger import logger
from blade_bench.llms import OpenAIGenConfig, AnthropicGenConfig, GeminiGenConfig
from .utils import get_conf_dir

load_dotenv()


def get_llm_config_from_conf_dict(conf_dict: dict):
    if (
        conf_dict.get("provider") == "openai"
        or conf_dict.get("provider") == "azureopenai"
    ):
        return OpenAIGenConfig(**conf_dict)
    elif conf_dict.get("provider") == "anthropic":
        return AnthropicGenConfig(**conf_dict)
    elif conf_dict.get("provider") == "gemini":
        return GeminiGenConfig(**conf_dict)
    else:
        raise ValueError(f"Unknown provider {conf_dict.get('provider')}")


def sanitize_provider(provider: str):
    if (
        provider.lower() == "openai"
        or provider.lower() == "default"
        or provider.lower() == "azureopenai"
        or provider.lower() == "azureoai"
    ):
        return "openai"
    elif provider.lower() == "gemini" or provider.lower() == "google":
        return "gemini"
    elif provider.lower() == "anthropic":
        return "anthropic"
    else:
        raise ValueError(
            f"Invalid provider '{provider}'.  Supported providers are 'gemini', 'openai', 'anthropic'."
        )


def get_llm_config(
    provider: str = None, model: str = None, textgen_config: TextGenConfig = None
):
    config = load_config()
    if provider is None:
        provider = (
            config["model"]["provider"] if "provider" in config["model"] else None
        )
    if provider is None:
        raise ValueError("Provider not specified in config file")
    provider = sanitize_provider(provider)
    models = (
        config["providers"][provider]["models"]
        if "providers" in config and provider in config["providers"]
        else {}
    )
    if model is None:
        model_name, model_conf = next(iter(models.items()))
        logger.info("Using default model '%s' for provider '%s'.", model_name, provider)
    else:
        model_name = model
        model_conf = models[model]
    model_conf["textgen_config"] = textgen_config
    config = get_llm_config_from_conf_dict(model_conf)
    return config


def load_config():
    try:
        config_path = os.environ.get("LLM_CONFIG_PATH", None)
        if config_path is None or os.path.exists(config_path) is False:
            config_path = os.path.join(get_conf_dir(), "config.default.yml")
            logger.info(
                "Info: LLM_CONFIG_PATH environment variable is not set to a valid config file. Using default config file at '%s'.",
                config_path,
            )
        if config_path is not None:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    logger.info("Loaded config from '%s'.", config_path)
                    return config
            except FileNotFoundError as file_not_found:
                logger.info(
                    "Error: Config file not found at '%s'. Please check the LLMX_CONFIG_PATH environment variable. %s",
                    config_path,
                    str(file_not_found),
                )
            except IOError as io_error:
                logger.info(
                    "Error: Could not read the config file at '%s'. %s",
                    config_path,
                    str(io_error),
                )
            except yaml.YAMLError as yaml_error:
                logger.info(
                    "Error: Malformed YAML in config file at '%s'. %s",
                    config_path,
                    str(yaml_error),
                )
        else:
            logger.info(
                "Info:LLM_CONFIG_PATH environment variable is not set. Please set it to the path of your config file to setup your default model."
            )
    except Exception as error:
        logger.info("Error: An unexpected error occurred: %s", str(error))
    return None
