"""
:copyright: (c) 2017 by Jumper Labs Ltd.
:license: Apache 2.0, see LICENSE.txt for more details.
"""
from __future__ import print_function

import os
import sys
from time import sleep
import calendar
import time
import requests
import logging
import json
import Queue
import threading
from __version__ import __version__ as jumper_current_version

API_URL = 'https://vlab.jumper.io/api/v2' if 'JUMPER_STAGING' not in os.environ else \
    'https://us-central1-jemu-web-app-staging.cloudfunctions.net/api/v2'


class WebException(Exception):
    pass


class AuthorizationError(WebException):
    def __init__(self, message):
        super(WebException, self).__init__(message)
        self.exit_code = 4
        self.message = message


class UnInitializedError(WebException):
    def __init__(self):
        print ("Failed to get user id. Please reach out to support@jumper.io for help")
        super(WebException, self).__init__("Failed to get user id. Please reach out to support@jumper.io for help")
        self.exit_code = 6
        self.message = "Failed to get user id. Please reach out to support@jumper.io for help"


class EmulatorGenerationError(WebException):
    def __init__(self, message):
        super(WebException, self).__init__(message)
        self.exit_code = 5
        self.message = message


class JemuWebApi(object):
    def __init__(self, jumper_token=None, api_url=API_URL, local_jemu=None):
        self._api_url = api_url
        self._token = jumper_token
        self._headers = {'Authorization': 'Bearer ' + self._token}
        self._user_uid = None
        self._local_jemu = local_jemu
        self._init()

    def _init(self):
        sys.stdout.write('Loading virtual device\n')
        sys.stdout.flush()
        logging.getLogger("requests").setLevel(logging.WARNING)
        res = requests.get(self._api_url + '/hello', headers=self._headers)
        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            if res.status_code == requests.codes['unauthorized'] or res.status_code == requests.codes['forbidden']:
                print ("Error: Authorization failed. Check the token in your config.json file")
                raise AuthorizationError("Error: Authorization failed. Check the token in the config.json file.")
            else:
                raise e

        self._user_uid = res.json()['userUid']
        self._threads = []
        self._events_queue = None
        self._init_events_queue()

    def _init_events_queue(self):
        if not self._local_jemu:
            self._events_queue = Queue.Queue()
            self._events_handler_should_run = True
            self._events_handler_thread = threading.Thread(target=self._event_sender)
            self._events_handler_thread.setDaemon(True)
            self._threads.append(self._events_handler_thread)
            self._events_handler_thread.start()

    def upload_file(self, filename, data):
        if self._user_uid is None:
            raise UnInitializedError

        headers = self._headers
        headers['Content-Type'] = 'application/octet-stream'
        res = requests.post(
            '{}/firmwares/{}/{}?zip={}'.format(self._api_url, self._user_uid, filename, 'true'),
            data=data,
            headers=headers
        )
        res.raise_for_status()

    def check_status(self, filename):
        if self._user_uid is None:
            raise UnInitializedError

        headers = self._headers
        headers['Content-Type'] = 'application/text'
        res = requests.get(
            '{}/firmwares/{}/{}/status'.format(self._api_url, self._user_uid, filename),
            headers=headers
        )
        return res

    def send_event(self, event_dict):
        if self._user_uid is None:
            raise UnInitializedError
        
        event_name = event_dict['event']
        event_labels = {}
        if "labels" in event_dict:
            event_labels = event_dict["labels"]
        event_labels['distinct_id'] = self._user_uid
        event_labels['sdk_version'] = jumper_current_version
        headers = self._headers
        headers['Content-Type'] = 'application/json'
        res = requests.post(
            '{}/analytics/{}/{}'.format(self._api_url, self._user_uid, event_name),
            headers=headers,
            json=event_labels
        )
        return res

    def check_error(self, filename):
        if self._user_uid is None:
            raise UnInitializedError

        headers = self._headers
        headers['Content-Type'] = 'application/text'
        res = requests.get(
            '{}/firmwares/{}/{}/error'.format(self._api_url, self._user_uid, filename),
            headers=headers
        )
        return res

    def get_jemu_version(self):
        headers = self._headers
        headers['Content-Type'] = 'application/text'
        res = requests.get(
            '{}/jemu-version'.format(self._api_url),
            headers=headers
        )
        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            return None
        return res.text

    def download_new_jemu(self, local_filename):
        if self._user_uid is None:
            raise UnInitializedError

        headers = self._headers
        headers['Content-Type'] = 'application/octet-stream'
        res = requests.get('{}/jemu/{}/zip_jemu'.format(self._api_url, self._user_uid), headers=headers)
        res.raise_for_status()
        signed_url = res.text
        res = requests.get(signed_url)
        res.raise_for_status()

        with open(local_filename, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def download_new_so(self, filename, local_filename):
        if self._user_uid is None:
            raise UnInitializedError

        headers = self._headers
        headers['Content-Type'] = 'application/octet-stream'

        res = requests.get(
            '{}/firmwares/{}/{}'.format(self._api_url, self._user_uid, filename),
            headers=headers)
        res.raise_for_status()
        signed_url = res.text
        res = requests.get(signed_url)

        with open(local_filename, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return True

    def add_event(self, message):
        if self._events_queue:
            self._events_queue.put(message)

    def _event_sender(self):
        while self._events_handler_should_run:
            try:
                cur_event = self._events_queue.get(True, timeout=0.2)
            except Queue.Empty:
                continue

            retries = 3
            while retries > 0:
                try:
                    self.send_event(cur_event)
                except Exception:
                    retries -= 1
                    sleep(1)
                else:
                    break

    def get_archived_emulator(self, fw_filename, fw_bin_data, so_dest, update_jemu, jemu_dest):
        signs = {"$", "#", "[", "]"}
        num_of_signs = fw_filename.count('.') - 1
        fw_filename = fw_filename.replace('.', '_', num_of_signs)
        for i in signs:
            fw_filename = fw_filename.replace(i, '_')

        fw_filename = str(int(calendar.timegm(time.gmtime()))) + '_' + fw_filename
        self.upload_file(fw_filename, fw_bin_data)

        sys.stdout.flush()
        status = 'Queded'
        while status != 'Done':
            status = self.check_status(fw_filename).text
            sys.stdout.write('.')
            sys.stdout.flush()
            sleep(0.25)
            if status == 'Fail':
                self.add_event({'event': 'firmware processing failed'})
                sys.stdout.write("FAILED")
                sys.stdout.write('\nVirtual device failed to start. Please reach out to support@jumper.io for help\n')
                sys.stdout.flush()
                error_string = self.check_error(fw_filename).text
                raise EmulatorGenerationError(error_string)
        jemu_filename = os.path.splitext(fw_filename)[0] + '.so.tgz'
        self.add_event({'event': 'firmware processing sucess'})

        self.download_new_so(jemu_filename, so_dest)
        self.add_event({'event': 'So download success'})
        if update_jemu:
            self.download_new_jemu(jemu_dest)
            self.add_event({'event': 'Jemu download success'})

        sys.stdout.write(' Done\n')
        sys.stdout.flush()

    def stop(self):
        self._events_handler_should_run = False
        self._stop_threads()

    def _stop_threads(self):
        for t in self._threads:
            if t.is_alive():
                t.join()
