from __future__ import print_function
import inspect
import json
import os
import sys
from collections import defaultdict
from contextlib import contextmanager

import luigi
from luigi.retcodes import run_with_retcodes as run_luigi
import requests

const_success_message = "Job ran successfully!"


class Monitor:
    recorded_events = defaultdict(list)
    notify_events = None

    def is_success_only(self):
        success_only = True
        for k, i in self.recorded_events.items():
            if k == 'SUCCESS' and len(i) > 0:
                success_only = success_only and True
            elif len(i) > 0:
                success_only = success_only and False
                break
        return success_only

    def has_missing_tasks(self):
        return True if self.recorded_events['DEPENDENCY_MISSING'] else False

    def has_failed_tasks(self):
        return True if self.recorded_events['FAILURE'] else False


def discovered(task, dependency):
    raise NotImplementedError


def missing(task):
    task = str(task)
    m.recorded_events['DEPENDENCY_MISSING'].append(task)


def present(task):
    raise NotImplementedError


def broken(task, exception):
    raise NotImplementedError


def start(task):
    raise NotImplementedError


def failure(task, exception):
    task = str(task)
    failure = {'task': task, 'exception': str(exception)}
    m.recorded_events['FAILURE'].append(failure)


def success(task):
    task = str(task)
    m.recorded_events['FAILURE'] = [failure for failure in m.recorded_events['FAILURE']
                                    if task not in failure['task']]
    m.recorded_events['DEPENDENCY_MISSING'] = [missing for missing in m.recorded_events['DEPENDENCY_MISSING']
                                    if task not in missing]
    m.recorded_events['SUCCESS'].append(task)


def processing_time(task, time):
    raise NotImplementedError


event_map = {
    "DEPENDENCY_DISCOVERED": {"function": discovered, "handler": luigi.Event.DEPENDENCY_DISCOVERED},
    "DEPENDENCY_MISSING": {"function": missing, "handler": luigi.Event.DEPENDENCY_MISSING},
    "DEPENDENCY_PRESENT": {"function": present, "handler": luigi.Event.DEPENDENCY_PRESENT},
    "BROKEN_TASK": {"function": broken, "handler": luigi.Event.BROKEN_TASK},
    "START": {"function": start, "handler": luigi.Event.START},
    "FAILURE": {"function": failure, "handler": luigi.Event.FAILURE},
    "SUCCESS": {"function": success, "handler": luigi.Event.SUCCESS},
    "PROCESSING_TIME": {"function": processing_time, "handler": luigi.Event.PROCESSING_TIME}
}


def set_handlers(events):
    if not isinstance(events, list):
        raise Exception("events must be a list")

    for event in events:
        if not event in event_map:
            raise Exception("{} is not a valid event.".format(event))
        handler = event_map[event]['handler']
        function = event_map[event]['function']
        luigi.Task.event_handler(handler)(function)


def format_message(max_print):
    job = os.path.basename(inspect.stack()[-1][1])
    text = ["Status report for {}".format(job)]
    if m.has_failed_tasks() and 'FAILURE' in m.notify_events:
        text.append("*Failures:*")
        if len(m.recorded_events['FAILURE']) > max_print:
            text.append("More than %d failures. Please check logs." % max_print)
        else:
            for failure in m.recorded_events['FAILURE']:
                text.append("Task: {}; Exception: {}".format(failure['task'], failure['exception']))
    if m.has_missing_tasks() and 'DEPENDENCY_MISSING' in m.notify_events:
        text.append("*Tasks with missing dependencies:*")
        if len(m.recorded_events['DEPENDENCY_MISSING']) > max_print:
            text.append("More than %d tasks with missing dependencies. Please check logs." % max_print)
        else:
            for missing in m.recorded_events['DEPENDENCY_MISSING']:
                text.append(missing)
    # if job successful add success message
    if m.is_success_only() and 'SUCCESS' in m.notify_events:
        text.append(const_success_message)
    formatted_text = "\n".join(text)
    if formatted_text == text[0]:
        return False
    return formatted_text





def send_message(slack_url, max_print, username=None):
    text = format_message(max_print)
    if not slack_url and text:
        print("slack_url not provided. Message will not be sent")
        print(text)
        return False
    if text:
        payload = {"text": text}
        if username:
            payload['username'] = username
        r = requests.post(slack_url, data=json.dumps(payload))
        if not r.status_code == 200:
            raise Exception(r.text)
    return True


m = Monitor()


@contextmanager
def monitor(events=['FAILURE', 'DEPENDENCY_MISSING', 'SUCCESS'], slack_url=None, max_print=5, username=None):
    if events:
        m.notify_events = events
        set_handlers(events)
    yield m
    send_message(slack_url, max_print, username)


def run():
    """Command line entry point for luigi-monitor"""
    events = ['FAILURE', 'DEPENDENCY_MISSING', 'SUCCESS']
    slack_url, max_print, username = parse_config()
    m.notify_events = events
    set_handlers(events)
    try:
        run_luigi(sys.argv[1:])
    except SystemExit:
        send_message(slack_url, max_print, username)


def parse_config():
    """Parse luigi-monitor config"""
    config = luigi.configuration.get_config()
    slack_url = config.get('luigi-monitor', 'slack_url', None)
    max_print = config.get('luigi-monitor', 'max_print', 5)
    username = config.get('luigi-monitor', 'username', None)
    return slack_url, max_print, username
