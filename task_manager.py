import logging

from PyQt5.QtCore import QRunnable, QThreadPool, QThread

from queue import Queue
from tasks.base_task import Task
from widgets.tasks_table import TasksTable


class TaskRunner(QRunnable):
    def __init__(self, tasks):
        super(TaskRunner, self).__init__()
        self.tasks = tasks

    def run(self):
        while True:
            try:
                task: Task = self.tasks.get_task()
                task_line = TasksTable.add_task(str(task), "")
                logging.info("Got task %s", task)
                task.start()
                TasksTable.remove_task(task_line)
            except:
                logging.exception("Failed to run task")


class TaskManagerSingleton(object):
    THREAD_POOL_SIZE = 10

    def __init__(self):
        self.tasks = Queue()
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(self.THREAD_POOL_SIZE)

    def add_task(self, task: Task):
        self.tasks.put(task)

    def get_task(self) -> Task:
        return self.tasks.get()

    def start(self):
        for _ in range(self.THREAD_POOL_SIZE):
            self.thread_pool.start(TaskRunner(self))


TaskManager = TaskManagerSingleton()


