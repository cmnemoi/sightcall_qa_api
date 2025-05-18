import importlib.metadata

from dotenv import load_dotenv

load_dotenv()

__version__ = importlib.metadata.version("sightcall_qa_api")
