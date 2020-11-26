from aiohttp import web

from app.queuemanager import QueueManager
from app.views import Handler
from app.config import Config


def init_app():
    app = web.Application()
    handler = Handler(app)
    app['queue'] = QueueManager(workers=Config.WORKERS)
    app.add_routes([
        web.get('/', handler.index),
        web.get('/get', handler.get_task_list),
        web.post('/put', handler.put_task)])
    return app


app = init_app()
