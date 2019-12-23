import logging
import traceback

from PyQt5.QtCore import QRunnable, QThreadPool, QThread

from queue import Queue
from tasks.base_task import Task


class TaskRunner(QRunnable):
    def __init__(self, tasks):
        super(TaskRunner, self).__init__()
        self.tasks = tasks

    def run(self):
        while True:
            task: Task = self.tasks.get_task()
            logging.info("Got task %s", task)
            task.start()


class TaskManagerSingleton(object):
    THREAD_POOL_SIZE = 10

    def __init__(self):
        self.tasks = Queue()
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(self.THREAD_POOL_SIZE)
        for _ in range(self.THREAD_POOL_SIZE):
            self.thread_pool.start(TaskRunner(self))

    def add_task(self, task: Task):
        self.tasks.put(task)

    def get_task(self) -> Task:
        return self.tasks.get()


TaskManager = TaskManagerSingleton()


