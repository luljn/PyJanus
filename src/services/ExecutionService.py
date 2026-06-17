# Execution service.

import asyncio
from dataclasses import dataclass
from datetime import datetime
import heapq
import threading
from typing import List, Callable, Any, Optional
import uuid 

from .Service import Service
from .Service import ServiceState

@dataclass
class Task(threading.Thread) :
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: int
    scheduled_time: Optional[datetime] = None
    
    def __lt__(self, other) : return self.priority < other.priority

"""_summary_: Manages thread execution.
"""
class ExecutionService(Service):
    
    # Constructor.
    def __init__(self) :
        
        super().__init__()
        self._task_queue: List[tuple] = []
        self._scheduled_tasks: List[tuple] = []
        self._running_tasks: set = set()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._counter = 0
    
    # To start the service.
    async def startAsync(self) -> None :
        
        self._set_state("STARTING")
        self._running = True
        self._worker_thread = threading.Thread(target=self._run_worker_loop, daemon=True)
        self._worker_thread.start()
        self._set_state("RUNNING")
        print("[" + self.name + "] Service started.")
    
    # To stop the service.
    async def stopAsync(self) -> None :
        
        self._set_state("STOPPING")
        self._running = False
        if self._worker_thread and self._worker_thread.is_alive() :
            await asyncio.to_thread(self._worker_thread.join, timeout=5.0)
        self._set_state("STOPPED")
        print("[" + self.name + "] Service stopped")  
    
    # Run worker loop.
    def _run_worker_loop(self) -> None :
        
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._worker_loop())
    
    # Worker loop.
    async def _worker_loop(self) -> None :
        
        while self._running :
            
            await self._process_scheduled_tasks()
            await self.executeTasks()
            await asyncio.sleep(0.1)
    
    # Process scheduled.
    async def _process_scheduled_tasks(self) -> None :
        
        now = datetime.now().timestamp()
        with self._lock :
            
            while self._scheduled_tasks and self._scheduled_tasks[0][0] <= now :
                
                _, _, task = heapq.heappop(self._scheduled_tasks)
                self._counter += 1
                heapq.heappush(self._task_queue, (task.priority, self._counter, task))
    
    # Execute task.
    def execute(self, func: Callable, *args, priority: int = 0, **kwargs) -> str :
        
        if self.state != ServiceState.RUNNING : raise RuntimeError("Execution Service isn't running")
        
        task = Task(id="task_"+ str(uuid.uuid4().hex[:8]), func=func, args=args, kwargs=kwargs, priority=priority)
        with self._lock:
            self._counter += 1
            heapq.heappush(self._task_queue, (priority, self._counter, task))
        return task.id
    
    # To schedule a task.
    def schedule(self, func: Callable, delay_seconds: float, *args, priority: int = 0, **kwargs) -> str :
        
        if self.state != ServiceState.RUNNING :
            
            raise RuntimeError("Execution Service isn't running")
        
        scheduled_time = datetime.now().timestamp() + delay_seconds
        task = Task(id="sched_" + str(uuid.uuid4().hex[:8]), func=func, args=args, kwargs=kwargs, priority=priority,
                    scheduled_time=datetime.fromtimestamp(scheduled_time))
        
        with self._lock :
            
            self._counter += 1
            heapq.heappush(self._scheduled_tasks, (scheduled_time, self._counter, task))
        
        return task.id
    
    # To execute tasks.
    async def executeTasks(self) -> int :
        
        executed_count = 0
        tasks_to_run = []
        
        with self._lock :
            
            while self._task_queue :
                
                _, _, task = heapq.heappop(self._task_queue)
                tasks_to_run.append(task)
        
        for task in tasks_to_run :
            
            await self._run_task(task)
            executed_count += 1
        
        return executed_count
    
    # To run a task.
    async def _run_task(self, task: Task) -> Any :
        
        current_task = asyncio.current_task()
        
        if current_task : self._running_tasks.add(current_task)
        
        try : return await asyncio.to_thread(task.func, *task.args, **task.kwargs)
        except Exception as e : print("Execution error of the task " + task.id + " : " + str(e))
        finally : 
            if current_task: self._running_tasks.discard(current_task)