import abc
import logging


class Task(object, metaclass=abc.ABCMeta):
    def start(self):
        try:
            self.run()
        except:
            logging.exception(f"Failed to run task {self.__class__.__name__}")

    @abc.abstractmethod
    def run(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}"
