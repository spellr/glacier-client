import abc
import consts
import logging

import boto3

from regions import Region
from widgets.tasks_table import TasksTable


class Task(object, metaclass=abc.ABCMeta):
    def __init__(self, region: Region):
        self.region = region
        self.task_row = None

    def start(self, task_row):
        self.task_row = task_row
        try:
            self.run()
        except:
            logging.exception(f"Failed to run task {self.__class__.__name__}")

    @abc.abstractmethod
    def run(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def update_task(self, size=""):
        TasksTable.update_task(self.task_row, str(self), size)

    def get_boto_client(self):
        session = boto3.session.Session()
        endpoint_url = None
        if consts.DEBUG:
            endpoint_url = 'http://localhost:5000'
        client = session.client('glacier', region_name=self.region.code, endpoint_url=endpoint_url,
                                aws_access_key_id=PUBLIC_KEY, aws_secret_access_key=SECRET_KEY)
        return client
