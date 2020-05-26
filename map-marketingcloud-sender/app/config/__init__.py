import os
from pathlib import Path


app_path = Path(__file__).parent.parent
SQL_PATH = os.path.join(app_path, 'data/sql/')