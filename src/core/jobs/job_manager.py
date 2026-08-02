from PySide6.QtCore import QObject, QThreadPool, QRunnable, Signal, Slot
from typing import Callable, Any

class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(int, str)
    
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        
    @Slot()
    def run(self):
        try:
            if 'progress_callback' in self.fn.__code__.co_varnames:
                self.kwargs['progress_callback'] = self.signals.progress.emit
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))

class JobManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.threadpool = QThreadPool()
        return cls._instance
        
    def submit(self, fn: Callable, on_finished: Callable = None, on_error: Callable = None, on_progress: Callable = None, *args, **kwargs):
        worker = Worker(fn, *args, **kwargs)
        if on_finished:
            worker.signals.finished.connect(on_finished)
        if on_error:
            worker.signals.error.connect(on_error)
        if on_progress:
            worker.signals.progress.connect(on_progress)
            
        self.threadpool.start(worker)

job_manager = JobManager()