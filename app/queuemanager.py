import asyncio
import functools


class QueueManager:
    def __init__(self, workers: int):
        self._queue = []
        self._semaphore = asyncio.Semaphore(workers)

    def put_task(self, task):
        self._queue.append(task)
        fut = asyncio.ensure_future(self.run(task))
        fut.add_done_callback(functools.partial(self.done_task, task))

    def done_task(self, task, _):
        self._queue.remove(task)

    def get_task_list(self):
        return self._queue

    async def run(self, task):
        async with self._semaphore:
            await task.run()
