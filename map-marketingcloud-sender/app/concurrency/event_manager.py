import threading

class EventManager:

    def __init__(self):
        self.lock = threading.Lock()
        self.events = {}

    def add_event(self, thread_name):
        with self.lock:
            self.events[thread_name] = threading.Event()

    def set(self, thread_name):
        with self.lock:
            self.events[thread_name].set()

    def is_set(self):
        is_set = []

        with self.lock:
            events = self.events.values()
            for event in events:
                is_set.append(event.is_set())

        return all(is_set)

