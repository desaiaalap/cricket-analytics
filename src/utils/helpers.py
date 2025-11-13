"""
Helper utility functions.
"""

import os
import json
import yaml
from typing import Any, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML or JSON file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    path = Path(config_path)

    if not path.exists():
        logger.error(f"Config file not found: {config_path}")
        return {}

    try:
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                config = yaml.safe_load(f)
            elif path.suffix == '.json':
                config = json.load(f)
            else:
                logger.error(f"Unsupported config format: {path.suffix}")
                return {}

        logger.info(f"Configuration loaded from {config_path}")
        return config

    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}


def save_config(config: Dict[str, Any], config_path: str, format: str = 'yaml'):
    """
    Save configuration to file.

    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
        format: File format ('yaml' or 'json')
    """
    try:
        with open(config_path, 'w') as f:
            if format == 'yaml':
                yaml.dump(config, f, default_flow_style=False)
            elif format == 'json':
                json.dump(config, f, indent=2)

        logger.info(f"Configuration saved to {config_path}")

    except Exception as e:
        logger.error(f"Error saving config: {e}")


def ensure_dir(directory: str):
    """
    Ensure directory exists, create if it doesn't.

    Args:
        directory: Directory path
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Directory ensured: {directory}")


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent.parent


def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """
    Setup logging configuration.

    Args:
        log_level: Logging level
        log_file: Optional log file path
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    handlers = [logging.StreamHandler()]

    if log_file:
        ensure_dir(os.path.dirname(log_file))
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers
    )

    logger.info(f"Logging setup complete - Level: {log_level}")
