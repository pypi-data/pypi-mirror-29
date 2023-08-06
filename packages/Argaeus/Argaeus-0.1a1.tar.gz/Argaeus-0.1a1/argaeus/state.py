import threading
import queue
from argaeus.controller.behavior.buttonbehavior import ButtonBehavior


class State:
    active_operation = None
    current_mode = None
    current_program = None
    current_schedule = None
    update_display = None
    behavior_queues = None

    def __init__(self):
        self.update_display = threading.Event()
        self.update_display.clear()

        self.behavior_queues = {}
        for b in ButtonBehavior:
            self.behavior_queues[b] = queue.Queue()

