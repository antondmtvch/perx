from aiohttp import web

from app import app, Config

if __name__ == '__main__':
    web.run_app(app, host=Config.HOST, port=Config.PORT)
