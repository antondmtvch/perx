from aiohttp import web
from app.task import Task
from app.exceptions import TaskValidationError


class Handler:
    def __init__(self, app):
        self.app = app

    async def index(self, request):
        response = {
            'available_methods': [
                {'path': '/get', 'method': 'GET', 'description': 'get all tasks in queue'},
                {'path': '/put', 'method': 'POST', 'description': 'put task on queue'},
            ]
        }
        return web.json_response(response)

    async def get_task_list(self, request):
        tasks = [task.serialize() for task in self.app['queue'].get_task_list()]
        return web.json_response({'tasks': tasks})

    async def put_task(self, request):
        data = await request.json()
        try:
            task = Task(**data)
        except TaskValidationError as ex:
            return web.json_response({'status': 400, 'message': str(ex)}, status=400)
        self.app['queue'].put_task(task)
        return web.json_response({'status': 200, 'message': 'OK'})

