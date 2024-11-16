import sys
import os

## Declaration required for using pytest_asyncio
pytest_plugins = ('pytest_asyncio',)

# Get absolute path of current file (__file__), get parent directory twice
# This allows importing modules from parent directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
