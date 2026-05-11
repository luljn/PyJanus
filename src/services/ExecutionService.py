import threading
import queue
from typing import Callable
from .Service import Service

class ExecutionService(Service):
    def __init__(self, max_workers: int = 4):
        super().__init__()
        self._task_queue = queue.Queue()
        self._workers = []
        self._max_workers = max_workers
        self._running = False

    def startAsync(self):
        self._running = True
        for _ in range(self._max_workers):
            t = threading.Thread(target=self._workerLoop, daemon=True)
            t.start()
            self._workers.append(t)
        print(f"[ExecutionService] démarré avec {self._max_workers} workers")

    def stopAsync(self):
        self._running = False
        for _ in self._workers:
            self._task_queue.put(None)
        for t in self._workers:
            t.join(timeout=2)
        self._workers.clear()
        print("[ExecutionService] arrêté")

    def awaitRunning(self):
        while not self._running:
            import time
            time.sleep(0.01)

    def execute(self, task: Callable) -> None:
        self._task_queue.put(task)

    def executeAgent(self, agent) -> None:
        if hasattr(agent, '_runLoop'):
            self.execute(agent._runLoop)

    def schedule(self, task: Callable, delay_seconds: float) -> None:
        def delayed():
            import time
            time.sleep(delay_seconds)
            self.execute(task)
        threading.Thread(target=delayed, daemon=True).start()

    def executeTasks(self) -> None:
        pass

    def getTaskCount(self) -> int:
        return self._task_queue.qsize()

    def _workerLoop(self):
        while self._running:
            try:
                task = self._task_queue.get(timeout=0.5)
                if task is None:
                    continue
                task()
            except queue.Empty:
                continue
