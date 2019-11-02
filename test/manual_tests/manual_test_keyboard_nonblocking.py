import logging
from queue import Queue
from time import sleep

from ms_logging.ms_logger_configurator import MsLoggerConfigurator
import sys
import threading


def add_input(queue, obj):
    while obj.thread_alive:
        reading_in = sys.stdin.read(1)
        print("read value %s" % reading_in)
        queue.put(reading_in)


class ThreadingExample(object):
    def __init__(self):
        self.thread_alive = False
        self.input_queue = None

    def foobar(self):
        self.input_queue = Queue()
        input_thread = threading.Thread(target=add_input, args=(self.input_queue, self))
        input_thread.daemon = True
        self.thread_alive = True
        input_thread.start()
        i = 0
        while True:
            sleep(0.001)
            i += 1
            if i > 1000:
                print("doing some work")
                i = 0
            if not self.input_queue.empty():
                text = ''
                while not self.input_queue.empty():
                    text += self.input_queue.get()
                text = text[:-1]
                print("here's what u gave! %s" % text)
                if text == "exit":
                    print("exiting")
                    self.thread_alive = False


if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    ThreadingExample().foobar()
