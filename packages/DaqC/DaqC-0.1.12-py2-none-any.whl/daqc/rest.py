import base64

from flask import Flask, send_from_directory, request, jsonify
import util
from settings import settings
import os.path
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from user import User
import secret
import logging
import re
import time
import collections
from rundb import RunDb
import itertools
import threading
import json

try:
    from flask_compress import Compress
except ImportError:
    class Compress:
        def __init__(self, _):
            print "Not compressing response. Consider installing flask-compress"


class RestApi:
    def __init__(self, **kwargs):
        self.app = Flask(__name__, static_path='', static_folder='')
        self.app.config['SECRET_KEY'] = kwargs.get("secret")
        Compress(self.app)

        self.log = logging.getLogger('werkzeug')
        self.log.setLevel(logging.ERROR)
        self.rundb = kwargs.get("rundb")
        self.use_rundb = util.RunDBState()
        if 'enabled' in settings['run_db'] and not settings['run_db']['enabled']:
            self.use_rundb.stop()

        self.login_manager = LoginManager(app=self.app)
        @self.login_manager.user_loader
        def load_user(id):
            return User(id)

        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend'))

        relay_cmd_log = self.constructRamLogger(settings['logs']['ucesb_log_lines'])
        logging.getLogger("relay_ucesb").addHandler(relay_cmd_log)
        file_cmd_log = self.constructRamLogger(settings['logs']['ucesb_log_lines'])
        logging.getLogger("file_ucesb").addHandler(file_cmd_log)
        go4_cmd_log = self.constructRamLogger(settings['logs']['go4_log_lines'])
        logging.getLogger("go4").addHandler(go4_cmd_log)
        backend_log = self.constructRamLogger(settings['logs']['n_log_lines'])
        logging.getLogger("backend").addHandler(backend_log)

        self.file_history = collections.deque(maxlen=settings['logs']['n_file_log'])

        for f in util.get_files_from_run_log(settings['logs']['runs_log']):
            self.file_history.append(f)

        self.vme = kwargs.get('vme')
        self.vme_lib = kwargs.get('vme_lib')
        self.relay = kwargs.get('relay')
        self.go4 = kwargs.get('go4')
        self.sync = kwargs.get('sync')
        self.mesytec = kwargs.get('mesytec')
        self.file_taker = kwargs.get('file_taker')
        self.watchdog = kwargs.get('watchdog')
        self.users = kwargs.get('users')
        self.trigger = kwargs.get('trigger')

        self.last_file = None
        self.last_info = {"facility": "IFA", "type": "Run"} if len(self.file_history) == 0 else self.file_history[-1].info

        t = threading.Thread(target=self.__build_status)
        t.daemon = True
        t.start()

        @self.app.route('/js/<path:path>')
        def js_static(path):
            return send_from_directory(os.path.join(static_dir, 'js'), path)


        @self.app.route('/css/<path:path>')
        def css_static(path):
            return send_from_directory(os.path.join(static_dir, 'css'), path)


        @self.app.route('/plugins/<path:path>')
        def ps_static(path):
            return send_from_directory(os.path.join(static_dir, 'plugins'), path)

        @self.app.route('/partials/<path:path>')
        def partials_static(path):
            return send_from_directory(os.path.join(static_dir, 'partials'), path)

        @self.app.route('/')
        def hello():
            return send_from_directory(static_dir, 'index.html')

        @self.app.route('/api/last_file_info')
        def last_file_info():
            return jsonify(self.last_info), 200

        @self.app.route('/api/update_trigger_names')
        def api_update_trigger_names():
            self.trigger.update_trigger_names()
            return jsonify({'names': self.trigger.get_trigger_names()}), 200

        @self.app.route('/api/trigger_names')
        def api_trigger_names():
            return jsonify({'names': self.trigger.get_trigger_names(), 'downscaling': self.trigger.get_downscaling()}), 200

        @self.app.route('/api/set_trigger', methods=['POST'])
        def api_set_trigger():
            if self.file_taker.is_running():
                return jsonify({'success': False, 'message': "Can not change triggers when taking file!"}), 400
            try:
                req = request.get_json()
                new_trigger = req['trigger']
                new_downscaling = req['downscaling']
                self.trigger.set_trigger(new_trigger, new_downscaling)
                return jsonify({'success': True, 'new_trigger': self.trigger.tpat, "downscaling": self.trigger.get_downscaling()}), 200
            except Exception as e:
                return jsonify({'success': False, 'message': e.message}), 400

        @self.app.route('/api/status')
        def api_status():
            response = self.app.response_class(
                response=self.status,
                status=200,
                mimetype='application/json'
            )
            return response

        @self.app.route('/api/logs')
        def api_logs():
            status = {}

            status.update({"synclog": list(self.sync.last)})
            status.update({"relay_ucesb_log": list(relay_cmd_log.get_messages())})
            status.update({"file_ucesb_log": list(file_cmd_log.get_messages())})
            status.update({"go4_log": list(go4_cmd_log.get_messages())})

            status.update({"log": list(backend_log.get_messages())})

            return jsonify(status), 200

        @self.app.route('/api/toggle', methods=['POST'])
        @login_required
        def api_start():
            restarts = {"go4": self.go4, "relay": self.relay}
            all_actions = dict(itertools.chain(restarts.iteritems(), {"sync": self.sync, "mesytec": self.mesytec, "rundb":self.use_rundb}.iteritems()))

            service = request.json.get("who")
            what = request.json.get("what")

            if what not in ["start", "stop", "restart"]:
                return jsonify({"success": False, "message": "No such action: '{}'".format(what)}), 400
            if service not in all_actions:
                return jsonify({"success": False, "message": "No such service: '{}'".format(service)}), 400

            if what == "restart":
                if service in restarts:
                    restarts[service].stop()
                    restarts[service].start()
                else:
                    return jsonify({"success": False, "message": "Service '{}' is not allowed to be restarted!".format(service)}), 400
            else:
                if what == "start":
                    all_actions[service].start()
                elif what == "stop":
                    all_actions[service].stop()
            return jsonify({"success": True}), 200


        @self.app.route('/api/start_file', methods=['POST'])
        @login_required
        def api_start_file():

            if self.file_taker.is_running():
                return jsonify(fail="File '{}' is already running. Stop it before you can start a new one!"
                               .format(self.file_taker.get_filename())), 400

            json = request.get_json()
            if "size" not in json:
                return jsonify(fail="No size attribute in client request"), 400

            file_size = json['size']
            if re.match(r"\d+[kMG]", file_size) is None:
                return jsonify(fail="Malformed size. Should be <integer>[kMG]"), 400

            self.file_taker.start(file_size)

            # Wait for up to 2seconds
            for _ in range(20):
                time.sleep(0.1)
                if self.file_taker.is_running():

                    self.last_file = None # We will now update the file taker instead of the lastest file
                    print("Start {}".format(self.last_file))
                    return jsonify({"file_size": file_size}), 200

            return jsonify(fail="Malformed size. Should be <integer>[kMG]"), 400


        @self.app.route('/api/send_info', methods=['POST'])
        @login_required
        def api_send_info():

            json = request.get_json()

            good_fields = ['beam', 'comments', 'experiment', 'facility',
                           'shifters', 'type', 'beam_e', 'beam_energy', 'beam_energy_unit', 'target']
            new_info = {k: json.get(k, None) for k in good_fields}

            self.last_info = new_info

            if self.last_file is None:
                self.file_taker.update_info(new_info)
            else:
                self.last_file.set_info(new_info)
                self.file_history.append(self.last_file)
                logging.getLogger("files").info(self.last_file.get_yaml())
                print(self.last_file.info)
                if self.use_rundb.shouldUpload:
                    self.last_file.set_on_log(lambda x: self.rundb.insert(self.last_file))
            return "Succes"


        @self.app.route('/api/stop_file', methods=['POST'])
        @login_required
        def api_stop_file():
            self.last_file = self.file_taker.stop()
            return "succes"


        @self.app.route('/api/login', methods=['POST'])
        def login():
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            if not self.users.validate(username, password):
                return jsonify({"msg": "Bad username or password"}), 401

            login_user(User(username))

            return jsonify({'login': True}), 200


        @self.app.route('/api/logout', methods=['POST'])
        @login_required
        def logout():
            logout_user()
            return jsonify({'login': False}), 200

        @self.login_manager.request_loader
        def load_user_from_request(request):
            """
            Load an user based on an API key in the request parameters.
            This can either be api_key in the request parameters
            or a Base64 encoded key in the **Authorization** header.
            :return:
            """

            # first, try to login using the api_key url arg
            api_key = request.args.get('api_key')
            if api_key:
                user = self.users.load_from_apikey(api_key)
                if user:
                    return user

            # next, try to login using Basic Auth
            api_key = request.headers.get('Authorization')
            if api_key:
                api_key = api_key.replace('Basic ', '', 1)
                print(api_key)
                try:
                    api_key = base64.b64decode(api_key)
                except TypeError:
                    pass
                user = self.users.load_from_apikey(api_key)
                if user:
                    return user

            # finally, return None if both methods did not login the user
            return None


        @self.app.route('/api/profile')
        @login_required
        def protected():
            return jsonify({'username': current_user.username}), 200

    def constructRamLogger(self, nLines, ):
        logger = util.RAMHandler(settings['logs']['ucesb_log_lines'])
        logger.setLevel(logging.DEBUG)
        logger.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        return logger

    def __build_status(self):
        while True:
            try:
                status = {}
                disk_space = util.get_disk_space(settings['file_taking']['data_dir'])[2] / 2 ** 20
                if disk_space != disk_space:
                    disk_message = "Not found!"
                else:
                    disk_message = "{} GB left".format(disk_space)
                status.update({"disk": {"message": disk_message}})

                status.update(self.watchdog.status())

                status["relay"]["message"] = "Processed %d Errors %d" % self.relay.progress()
                status["sync"]["message"] = self.sync.status()
                status["vme"]["message"] = self.vme.status()
                status["mesytec"]["message"] = self.mesytec.status()
                status["mesytec"]["last_check"] = self.mesytec.last_check()
                status["vme"]["host"] = self.vme.get_name()
                status["sync"]["target"] = settings['sync']['destinations']
                status["vme_lib"]["stats"] = self.vme_lib.status()
                status["vme_lib"]["message"] = self.vme_lib.get_message()

                status.update({'trigger': {
                    'status': self.trigger.tpat,
                    'active': self.trigger.get_active_trigger(),
                'downscaling': self.trigger.get_downscaling()
                }})

                status["data_dir"] = settings['file_taking']['data_dir']
                f_events, f_errors = self.file_taker.progress()
                if self.file_taker.is_stopping():
                    f = {"status": "stopping", "message": "stopping"}
                else:
                    f = {"name": self.file_taker.prefix(),
                         "progress": f_events,
                         "errors": f_errors,
                         "start_time": self.file_taker.starttime(),
                         "status": "running" if self.file_taker.is_running() else "stopped"}

                status.update({"file": f})
                status.update({"filelog": [x.info for x in self.file_history]})

                status['readout_lib'] = self.vme_lib.get_name().lower()
                status.update({"rundb": {"status": "running" if self.use_rundb.shouldUpload else "stopped"}})

                self.status = json.dumps(status)
            except Exception as e:
                logging.getLogger("backend").error("Error when trying to create status: {}".format(e.message))

            time.sleep(1)
