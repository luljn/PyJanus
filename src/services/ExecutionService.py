import threading
import asyncio
import heapq
import uuid  
from dataclasses import dataclass
from datetime import datetime
from typing import List, Callable, Any, Optional
from .Service import Service
@dataclass
class Task:
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: int
    scheduled_time: Optional[datetime] = None
    
    def __lt__(self, other):
        return self.priority < other.priority

class ExecutionService(Service):
    
    def __init__(self):
        super().__init__()
        self._task_queue: List[tuple] = []
        self._scheduled_tasks: List[tuple] = []
        self._running_tasks: set = set()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.Lock()
        self._counter = 0
    
    async def startAsync(self) -> None:
        self._set_state("STARTING")
        self._running = True
        self._worker_thread = threading.Thread(target=self._run_worker_loop, daemon=True)
        self._worker_thread.start()
        self._set_state("RUNNING")
    
    async def stopAsync(self) -> None:
        self._set_state("STOPPING")
        self._running = False
        if self._worker_thread and self._worker_thread.is_alive():
            await asyncio.to_thread(self._worker_thread.join, timeout=5.0)
        self._set_state("STOPPED")
    
    async def awaitRunning(self) -> None:
        """Attend que le service soit en état RUNNING"""
        while True:
            current_state = self._state if isinstance(self._state, str) else self._state.value
            if current_state == "RUNNING":
                return
            if current_state in ["STOPPED", "FAILED"]:
                raise RuntimeError("ExecutionService stopped or failed")
            await asyncio.sleep(0.1)

    def _run_worker_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._worker_loop())
    
    async def _worker_loop(self) -> None:
        while self._running:
            await self._process_scheduled_tasks()
            await self.executeTasks()
            await asyncio.sleep(0.1)
    
    async def _process_scheduled_tasks(self) -> None:
        now = datetime.now().timestamp()
        with self._lock:
            while self._scheduled_tasks and self._scheduled_tasks[0][0] <= now:
                _, _, task = heapq.heappop(self._scheduled_tasks)
                self._counter += 1
                heapq.heappush(self._task_queue, (task.priority, self._counter, task))
    
    def execute(self, func: Callable, *args, priority: int = 0, **kwargs) -> str:
        if self.state != ServiceState.RUNNING:
            raise RuntimeError("ExecutionService n'est pas actif")
        
        task = Task(id=f"task_{uuid.uuid4().hex[:8]}", func=func, args=args, kwargs=kwargs, priority=priority)
        with self._lock:
            self._counter += 1
            heapq.heappush(self._task_queue, (priority, self._counter, task))
        return task.id
    
    def schedule(self, func: Callable, delay_seconds: float, *args, priority: int = 0, **kwargs) -> str:
        if self.state != ServiceState.RUNNING:
            raise RuntimeError("ExecutionService n'est pas actif")
        
        scheduled_time = datetime.now().timestamp() + delay_seconds
        task = Task(id=f"sched_{uuid.uuid4().hex[:8]}", func=func, args=args, kwargs=kwargs, priority=priority,
                    scheduled_time=datetime.fromtimestamp(scheduled_time))
        with self._lock:
            self._counter += 1
            heapq.heappush(self._scheduled_tasks, (scheduled_time, self._counter, task))
        return task.id
    
    async def executeTasks(self) -> int:
        executed_count = 0
        tasks_to_run = []
        
        with self._lock:
            while self._task_queue:
                _, _, task = heapq.heappop(self._task_queue)
                tasks_to_run.append(task)
        
        for task in tasks_to_run:
            await self._run_task(task)
            executed_count += 1
        return executed_count
    
    async def _run_task(self, task: Task) -> Any:
        current_task = asyncio.current_task()
        if current_task:
            self._running_tasks.add(current_task)
        try:
            return await asyncio.to_thread(task.func, *task.args, **task.kwargs)
        except Exception as e:
            print(f"Erreur d'exécution de la tâche {task.id}: {e}")
        finally:
            if current_task:
                self._running_tasks.discard(current_task)