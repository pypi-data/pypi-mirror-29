import base64
import logging
import requests
from threading import Thread
from time import sleep
import json

class RunDb:
    def __init__(self, **kwargs):
        host = kwargs.get('url')
        if host is None:
            raise ValueError("Missing RunDB url")

        api_version = kwargs.get('api_version')
        if api_version is None:
            raise ValueError("Missing RunDB api version")

        self.api_key = kwargs.get('api_key')
        if self.api_key is None:
            raise ValueError("Missing RunDB api key")

        self.encoded_api_key = base64.b64encode(self.api_key)

        if api_version == 1:
            self.insert_url = "{}/api/v1/insert_run".format(host)
        else:
            raise ValueError("DaqC currently only support version 1 of the RunDB API")

        self.retries = kwargs.get('retries', 10)
        self.wait = kwargs.get('retry_wait', 5)
        self.backend_log = logging.getLogger("backend")

    def insert(self, f):
        headers = {'Authorization': 'Basic {}'.format(self.encoded_api_key), "Content-Type": "application/json"}

        def poster():
            try:
                for _ in range(self.retries):
                    payload = f.info
                    payload.update({'log_file': f.log})
                    r = requests.post(self.insert_url, data=json.dumps(payload), headers=headers)
                    if r.status_code == 200:
                        self.backend_log.info("Successfully added run to RunDB")
                        return
                    else:
                        self.backend_log.warn("Failed writing data to RunDB. Will retry")
                        self.backend_log.error("Error message: {}".format(r.text))
                        sleep(self.wait)
            except requests.ConnectionError:
                self.backend_log.warn("Connection error to RunDB!")
                return
            self.backend_log.warn("Failed writing data to RunDB!")

        t = Thread(target=poster)
        t.daemon = False
        t.start()



class MockRunDb:
    def __init__(self, **kwargs):
        pass

    def insert(self, f):
        print "Insertion in RunDB {}".format(f)