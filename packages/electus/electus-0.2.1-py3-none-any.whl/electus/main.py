import os
import sys
import json
import platform
from datetime import datetime
import logging, logging.handlers

import requests

from .config import Library, Job


class Electus(object):

    def __init__(self, library_conf=None, job_conf=None, log_file=None, url=None):
        """Generates an alert if a combination of features are found in a set of events.

        Args:
            library_conf (str): Path to a library configuration file.
            job_conf (str): Path to a job configuration file.
            log_file (str): Path to a file to write the alerts to.
            url (str): If an electus server is configured at the url it will fetch the relevant configuration files and
                       push alerts to that server.
        """
        self.url = url

        if self.url is None:
            if library_conf is None or job_conf is None:
                raise ValueError('Library_conf and job_conf must be specified. Alternatively, a URL to an electus server can be provided.')
        else:
            library_conf = requests.get(self.url + 'electus/api/v1.0/library').json()
            job_conf = requests.get(self.url + 'electus/api/v1.0/jobs').json()

        self.job_config = job_conf
        self.library = library_conf

        self.get_jobs()

        self.log = log_file

        self.logger = None
        #self.logger = logging.getLogger("")
        #self.logger.setLevel(logging.DEBUG)

        self.events = []
        self.alerts = []
        self.alert_dicts = []

    @property
    def job_config(self):
        """A dictionary loaded from the job_conf file."""
        return self._job_config

    @job_config.setter
    def job_config(self, job_conf):
        if isinstance(job_conf, dict):
            self._job_config = job_conf
        elif os.path.exists(job_conf):
            with open(job_conf, 'r') as f:
                self._job_config = json.load(f)
        else:
            raise IOError('Job file {} not found'.format(job_conf))

    @property
    def library(self):
        """A list of initialized LibraryDefinition objects loaded from lib_conf"""
        return self._library

    @library.setter
    def library(self, lib):
        self._library = Library(lib).library

    @property
    def log(self):
        """Path to a file to write the alerts to."""
        return self._log

    @log.setter
    def log(self, log_file):
        if log_file is not None:
            self._log = log_file
        else:
            self._log = None

    @property
    def url(self):
        """If an electus server is configured at the url it will fetch the relevant configuration files
           and push alerts to that server.
        """
        return self._url

    @url.setter
    def url(self, u):
        if u is None:
            self._url = None
        elif not isinstance(u, str):
            raise ValueError('URL must be a string')
        else:
            if u[-1] != '/':
                u += '/'

            self._url = u

    def get_jobs(self):
        """Creates a list of Job objects based on the job_config dictionary."""
        self.jobs = []
        for job_name in self.job_config:
            self.jobs.append(Job(name=job_name, job_config=self.job_config[job_name], library=self.library))

    def evaluate_event(self, event):
        """Check if the event generates an Alert.

        Args:
            event (dict): An event which should be a python dictionary.
        Returns:
            A list of Alert objects which is all of the alerts that have been generated.
        """
        self.events.append(event)
        alerts_for_event = []
        
        for job in self.jobs:
            alert = job.combination_engine.alert(self.events)

            if alert is not None:
                self.alert_dicts.append(alert.to_dict())
                self.alerts.append(alert)
                alerts_for_event.append(alert)

                if self.log:
                    with open(self.log, 'w') as f:
                        json.dump(self.alert_dicts, f, indent=4)

                elif self.url:
                    payload = {'timestamp': datetime.utcnow().isoformat(), 'hostname': platform.node(), 'alert': alert.to_dict()}
                    r = requests.post(self.url + 'electus/api/v1.0/alert', json=payload)

                elif self.logger:
                    payload = {'timestamp': datetime.utcnow().isoformat(), 'hostname': platform.node(),
                               'alert': alert.to_dict()}

                    self.logger.warning(json.dumps(payload))

                else:
                    pass
        return alerts_for_event


















