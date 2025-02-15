import logging
import subprocess
import sys

logger = logging.getLogger(__name__)

def check_venv():
    """Check if inside a virtual environment and list installed packages."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_path = sys.prefix
        logger.debug(f"You are inside a virtual environment: {venv_path}\n")

        # Show installed packages using pip
        logger.debug("Installed packages:")
        subprocess.run([sys.executable, "-m", "pip", "list"])
    else:
        logger.debug("You are not inside a virtual environment.")
