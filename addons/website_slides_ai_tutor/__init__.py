# -*- coding: utf-8 -*-

import os
import logging
from pathlib import Path

# Load environment variables from .env file using python-dotenv
def load_env_file():
    try:
        # Try to import python-dotenv
        try:
            from dotenv import load_dotenv
        except ImportError:
            logging.getLogger(__name__).warning("python-dotenv not installed. Falling back to manual loading.")
            # Fallback to manual loading
            _manual_load_env()
            return
        
        # Get the Odoo root directory (where odoo-bin is located)
        # Path structure: /home/claude/git/odoo/15.0/addons/website_slides_ai_tutor/__init__.py
        # We need to go up 2 levels to get to /home/claude/git/odoo/15.0/
        env_file = Path(__file__).parents[2] / '.env'
        
        if env_file.exists():
            load_dotenv(env_file)
            logging.getLogger(__name__).info(f"Loaded environment variables from {env_file} using python-dotenv")
        else:
            logging.getLogger(__name__).warning(f"No .env file found at {env_file}")
    except Exception as e:
        logging.getLogger(__name__).error(f"Error loading .env file: {e}")

def _manual_load_env():
    """Fallback manual .env loading if python-dotenv is not available"""
    try:
        env_file = Path(__file__).parents[3] / '.env'  # Go up to Odoo root
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")  # Remove quotes
                        os.environ.setdefault(key, value)
            logging.getLogger(__name__).info(f"Loaded environment variables from {env_file} (manual)")
        else:
            logging.getLogger(__name__).warning(f"No .env file found at {env_file}")
    except Exception as e:
        logging.getLogger(__name__).error(f"Error manually loading .env file: {e}")

# Load environment variables when module is imported
load_env_file()

from . import models
from . import controllers
