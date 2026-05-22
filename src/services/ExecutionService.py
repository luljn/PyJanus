# Execution Service

import threading
import asyncio
import heapq
from dataclasses import dataclass
from datetime import datetime
from typing import List, Callable, Any, Optional
from .Service import Service

@dataclass
class Task:
    """Structure d'une tâche à exécuter"""
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
        self._task_queue: List[Task] = []  # File d'attente des tâches
        self._scheduled_tasks: List[tuple] = []  # Tâches planifiées (timestamp, task)
        self._running_tasks: set = set()  # Tâches en cours d'exécution
        self._worker_thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._running = False
        self._lock = threading.Lock()
    
    def startAsync(self) -> None:
        """Démarre le service d'exécution"""
        self._set_state("STARTING")
        self._running = True
        
        # Créer et démarrer le thread de travail
        self._worker_thread = threading.Thread(target=self._run_worker_loop, daemon=True)
        self._worker_thread.start()
        
        self._set_state("RUNNING")
    
    def stopAsync(self) -> None:
        """Arrête le service d'exécution"""
        self._set_state("STOPPING")
        self._running = False
        
        # Attendre la fin du thread
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)
        
        self._set_state("STOPPED")
    
    def awaitRunning(self) -> None:
        """Attend que le service soit en état RUNNING"""
        while self._state != "RUNNING":
            if self._state in ["STOPPED", "FAILED"]:
                raise RuntimeError("ExecutionService stopped or failed")
            import time
            time.sleep(0.1)
    
    def _run_worker_loop(self) -> None:
        """Boucle de travail dans un thread séparé"""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._worker_loop())
    
    async def _worker_loop(self) -> None:
        """Boucle principale du worker"""
        while self._running:
            await self._process_scheduled_tasks()
            await self.executeTasks()
            await asyncio.sleep(0.1)
    
    async def _process_scheduled_tasks(self) -> None:
        """Traite les tâches planifiées dont l'heure est arrivée"""
        now = datetime.now().timestamp()
        
        with self._lock:
            while (self._scheduled_tasks and 
                   self._scheduled_tasks[0][0] <= now):
                _, task = heapq.heappop(self._scheduled_tasks)
                heapq.heappush(self._task_queue, task)
    
    def execute(self, func: Callable, *args, priority: int = 0, **kwargs) -> str:
        """Exécute une tâche immédiatement"""
        if not self._running:
            raise RuntimeError("ExecutionService n'est pas en état RUNNING")
        
        task = Task(
            id=f"task_{datetime.now().timestamp()}",
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority
        )
        
        with self._lock:
            heapq.heappush(self._task_queue, task)
        
        return task.id
    
    def schedule(self, func: Callable, delay_seconds: float, *args, priority: int = 0, **kwargs) -> str:
        """Planifie une tâche pour exécution future"""
        if not self._running:
            raise RuntimeError("ExecutionService n'est pas en état RUNNING")
        
        scheduled_time = datetime.now().timestamp() + delay_seconds
        
        task = Task(
            id=f"scheduled_{datetime.now().timestamp()}",
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            scheduled_time=datetime.fromtimestamp(scheduled_time)
        )
        
        with self._lock:
            heapq.heappush(self._scheduled_tasks, (scheduled_time, task))
        
        return task.id
    
    async def executeTasks(self) -> int:
        """Exécute toutes les tâches en attente (asynchrone)"""
        executed_count = 0
        tasks_to_run = []
        
        with self._lock:
            while self._task_queue:
                task = heapq.heappop(self._task_queue)
                tasks_to_run.append(task)
        
        for task in tasks_to_run:
            await self._run_task(task)
            executed_count += 1
        
        return executed_count
    
    def executeTasksSync(self) -> int:
        """Version synchrone de executeTasks (pour appel depuis thread)"""
        if not self._loop:
            return 0
        
        future = asyncio.run_coroutine_threadsafe(self.executeTasks(), self._loop)
        return future.result()
    
    async def _run_task(self, task: Task) -> Any:
        """Exécute une tâche individuelle"""
        current_task = asyncio.current_task()
        self._running_tasks.add(current_task)
        
        try:
            # Exécuter la fonction dans un thread pour ne pas bloquer
            result = await asyncio.to_thread(task.func, *task.args, **task.kwargs)
            return result
        except Exception as e:
            print(f"Erreur dans la tâche {task.id}: {e}")
            raise
        finally:
            self._running_tasks.discard(current_task)
    
    def getTaskCount(self) -> int:
        """Retourne le nombre de tâches en attente"""
        with self._lock:
            return len(self._task_queue) + len(self._scheduled_tasks)
    
    def getRunningTaskCount(self) -> int:
        """Retourne le nombre de tâches en cours d'exécution"""
        return len(self._running_tasks)
    
    def clear(self) -> None:
        """Vide toutes les files d'attente"""
        with self._lock:
            self._task_queue.clear()
            self._scheduled_tasks.clear()