import glob
import json
import os
import subprocess

from subprocess import PIPE

import dotenv
import loguru

from flask import Blueprint, abort, render_template, send_file, session, redirect, request

from auth.auth import authenticate
from plugins.database import Database

dotenv.load_dotenv()

_bp = Blueprint('class', __name__, url_prefix='/class')
logger = loguru.logger
available_tests = set()


TEST_DIR = os.getenv('TEST_DIR')
MAX_TIMEOUT_SECONDS = int(os.getenv('MAX_TIMEOUT_SECONDS'))


class ClassHandler:
    def __init__(self, tests):
        global available_tests
        available_tests = tests
        logger.info('Initialized {}', __name__)

    def route(self) -> Blueprint:
        return _bp


def get_test_cases(class_name, assn_num):
    path = f'test/{class_name}/{assn_num}'
    path = os.path.abspath(f'{path}/testcases.json')
    with open(path, 'r') as f:
        j = json.load(f)
    return j


def run_subprocess(cmds, directory):
    process = subprocess.Popen(
        cmds,
        stdout=PIPE,
        stderr=PIPE,
        cwd=os.path.abspath(directory)
    )

    try:
        output, error = process.communicate(timeout=MAX_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        logger.error('Killing: {}', process.pid)
        process.kill()
    return process.returncode, output, error


@_bp.route('/<string:class_id>/<string:assn_id>/attempt', methods=['GET'])
@authenticate
def _assignment_attempt(class_id, assn_id):
    logger.info("{} {}", class_id, assn_id)
    user = session.get("user")
    username = user.get("email")

    with Database() as db:
        attempt = db.get_latest_attempt(username, class_id, assn_id)

        if attempt.get("code", None) is not None:
            attempt = attempt.get("code")
        else:
            attempt = _class_files(class_id, assn_id, extra_file='template')

    return attempt


@_bp.route('/', methods=['GET'])
@authenticate
def _classes():
    user = session.get("user").get("email")
    with Database() as db:
        assignments = db.get_classes_not_registered(user)
    return json.dumps(assignments)


@_bp.route('/registered', methods=['GET'])
@authenticate
def _registered_class():
    user = session.get("user").get("email")
    with Database() as db:
        classes = db.get_registered_classes(user)
    return json.dumps(classes)


@_bp.route('/<string:class_id>', methods=['GET'])
@authenticate
def _assignments(class_id):
    with Database() as db:
        assignments = db.get_assignments(class_id)
    return json.dumps(assignments)


@_bp.route('/<string:class_id>/register', methods=['POST'])
@authenticate
def _register_class(class_id):
    user = session.get("user").get("email")

    with Database() as db:
        class_info = db.get_class_info(class_id)
    if class_info is not None:
        with Database() as db:
            db.register_class(user, class_id)
        return "success", 201
    else:
        return "fail", 404


@_bp.route('/<string:class_name>/<string:assn_num>/prompt', methods=['GET'])
@authenticate
def _class_files(class_name, assn_num, extra_file='prompt'):
    path = f'test/{class_name}/{assn_num}'
    if extra_file in ['prompt', 'template']:
        path = os.path.abspath(f'{path}/{extra_file}')
        f = glob.glob(path + '*')
        return send_file(f[0])
    return abort(404)


@_bp.route('/<string:class_name>/<string:assn_num>', methods=['GET', 'POST'])
@authenticate
def _class_assignment(class_name, assn_num):
    path = f'{class_name}/{assn_num}'
    if path not in available_tests:
        return abort(404)
    if request.method == 'POST':
        body = request.get_json(force=True)
        harness_method = body.get('method')
        if harness_method not in ['test', 'submit']:
            return json.dumps({'status': 'error',
                               'output': ['Invalid harness method']}), 401

        dotenv.load_dotenv(os.path.abspath(f'{TEST_DIR}/{path}/config'))

        with open(os.path.abspath(f'{TEST_DIR}/{path}/{os.getenv("FILE_NAME")}'), 'w') as f:
            f.write(body.get('code'))

        test_case_outputs = []
        score = 0
        maxscore = 0
        if harness_method == 'submit':
            with open(os.path.abspath(f'{TEST_DIR}/{path}/testcases.json'), 'r') as f:
                for testcase in json.load(f):
                    logger.info("Running {}", testcase.get('file'))
                    ret, output, error = run_subprocess(
                        ['python3', '-m', 'unittest', '-v', testcase.get('file')], f'{TEST_DIR}/{path}')
                    test_case_outputs.append(
                        {
                            "id": testcase.get('file'),
                            "file": testcase.get('file'),
                            "name": testcase.get("name"),
                            "score": testcase.get('maxscore') if ret == 0 else 0,
                            "maxscore": testcase.get('maxscore')
                        }
                    )
                    logger.info("Output: {}", ret)
                    score += testcase.get('maxscore') if ret == 0 else 0
                    maxscore += testcase.get('maxscore')

                data = {
                    "testcases": test_case_outputs,
                    "currScore": score,
                    "code": body.get("code")
                }
                with Database() as db:
                    db.set_latest_attempt(
                        session.get("user").get("email"),
                        assn_num,
                        json.dumps(data),
                        score=score,
                        maxscore=maxscore
                    )
        else:
            ret, output, error = run_subprocess(
                ['bash', './run.sh', harness_method], f'{TEST_DIR}/{path}')

        return _create_return_json(ret, output, error, harness_method, score=score, data=test_case_outputs), 201

    # GET
    test_cases = get_test_cases(class_name, assn_num)
    curr_score = 0
    with Database() as db:
        name = db.get_class_info(class_name).get("name")
        prev_attempt = db.get_latest_attempt(
            session.get("user").get("email"), class_name, assn_num)
        if prev_attempt:
            curr_score = prev_attempt.get("currScore")
            test_cases = prev_attempt.get("testcases")

    data = {
        "assignment": assn_num,
        "name": name,
        "currScore": curr_score,
        "user": session.get("user"),
        "testcases": test_cases,
        "maxScore": sum([tc.get('maxscore') for tc in test_cases])
    }
    return render_template('editor.html', data=data)


def _create_return_json(return_code, output, error, harness_method, score=0, data=None):
    logger.info('Return code: {}', return_code)
    status = 'success'
    if harness_method == 'submit':
        output = b'Hidden'
    elif return_code is None:
        status = 'timeout'
        output = b"Submission timed out"
    elif return_code != 0:
        status = 'error'
        output = error
    return json.dumps({"status": status, "output": output.decode("utf-8").split('\n'), "score": score, "data": data})
