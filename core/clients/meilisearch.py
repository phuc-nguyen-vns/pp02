import meilisearch
import sys, os
from pathlib import Path
sys.path.append(Path(os.getcwd(),"PP02").as_posix())
from config.settings import settings


MeiliClient = meilisearch.Client(settings.meilisearch_url, settings.meilisearch_token)
