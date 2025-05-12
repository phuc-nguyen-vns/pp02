from core.utils.config_loader import load_yaml_config
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "categories.yml"

config = load_yaml_config(CONFIG_PATH)
CATEGORIES_LIST = config.get("categories", [])
print(CATEGORIES_LIST)