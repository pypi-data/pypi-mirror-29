"Implementation of the celery3 execution engine plugin."

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from itertools import repeat
from cosmic_ray.execution.execution_engine import ExecutionEngine
from cosmic_ray.worker import worker_process


class cosmic_ray_parallel_engine(ExecutionEngine):
    "The parallel execution engine."
    def __call__(self, timeout, pending_work_items, config):
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            yield from executor.map(worker_process,
                                    pending_work_items,
                                    repeat(timeout),
                                    repeat(config))
