import os
import json

from dotenv import load_dotenv
from flask import make_response
from kasasa_common import logger

from config.shared_text import WorkerPid
from service.application import create_application

load_dotenv()
app = create_application()


@app.route('/', strict_slashes=False)
def root():
    response = make_response(json.dumps({'status': 'root'}), 200)
    return response


@app.route('/admin/health', strict_slashes=False)
def health():
    response = make_response(json.dumps({'status': 'ok'}), 200)
    return response


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return 500
    else:
        return 200


@app.route('/admin/ready', methods=['GET'])
def ready():
    status_code = 503
    response_ready = make_response(json.dumps({'status': 'issues occur'}), 500)

    try:
        with open(WorkerPid.FILE_PATH, 'r') as pid_file:
            file_read_pid = int(pid_file.read())
            status_code = check_pid(file_read_pid)
    except Exception as e:
        logger.exception("Error checking process ID file.", e)

    if status_code == 200:
        response_ready = make_response(json.dumps({'status': 'ok'}), 200)
    elif status_code == 503:
        response_ready = make_response(json.dumps({'status': 'worker process is not running'}), 503)
    return response_ready
