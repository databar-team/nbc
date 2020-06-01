import os

from dotenv import load_dotenv

from config.shared_text import WorkerPid

load_dotenv()

WORKER_PID = str(os.getpid())
with open(WorkerPid.FILE_PATH, 'w') as out_file:
    print('Worker app PID:', WORKER_PID)
    out_file.write(WORKER_PID)
