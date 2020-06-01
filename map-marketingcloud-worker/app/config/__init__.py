import os
from pathlib import Path

title = 'MAP Sales Force Marketing Cloud Integration'
version = 1

description = f"""<h3>API for MAP Sales Force Marketing Cloud Integration</h3>"""

app_path = Path(__file__).parent
WORKER_SQL_PATH = os.path.join(app_path, 'worker/data/sql/')
