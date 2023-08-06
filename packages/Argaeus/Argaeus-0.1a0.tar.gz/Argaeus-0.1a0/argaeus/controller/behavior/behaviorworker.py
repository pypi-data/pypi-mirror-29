import threading


class BehaviorWorker:
    _state = None
    _verbose = None
    _EXECUTE_BEHAVIOR = None
    _behavior_executor = None
    _worker_thread = None

    def __init__(self, verbose, state, execute_behavior, behavior_executor):
        self._verbose = verbose
        self._state  = state
        self._EXECUTE_BEHAVIOR = execute_behavior
        self._behavior_executor = behavior_executor
        if self._verbose:
            print("BehaviorWorker.__init__ - initializing instance ('{}').".format(self._EXECUTE_BEHAVIOR))

        self._worker_thread = threading.Thread(target=self._worker)

    def _worker(self):
        if self._verbose:
            print("BehaviorWorker('{}') - started worker".format(self._EXECUTE_BEHAVIOR))
        while True:
            item = self._state.behavior_queues[self._EXECUTE_BEHAVIOR].get()
            if self._verbose:
                print("BehaviorWorker('{}') - worker received item '{}'.".format(self._EXECUTE_BEHAVIOR, item))
            if item is None:
                break
            self._behavior_executor(item)
            self._state.behavior_queues[self._EXECUTE_BEHAVIOR].task_done()
        if self._verbose:
            print("BehaviorWorker('{}') - stopped worker".format(self._EXECUTE_BEHAVIOR))

    def start(self):
        if self._verbose:
            print("BehaviorWorker.starting for '{}'".format(self._EXECUTE_BEHAVIOR))
        self._worker_thread.start()

    def stop(self):
        self._state.behavior_queues[self._EXECUTE_BEHAVIOR].put(None)
        self._worker_thread.join()
        if self._verbose:
            print("BehaviorWorker.stopped for '{}'".format(self._EXECUTE_BEHAVIOR))
