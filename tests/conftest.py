from functools import partial

import trio
import pytest
from flask import Flask, jsonify, request, make_response
from werkzeug.serving import BaseWSGIServer, WSGIRequestHandler

from async_vk_api.api import Api


server_ready = trio.Event()


class Handler(WSGIRequestHandler):

    protocol_version = 'HTTP/1.1'


class Server(BaseWSGIServer):

    def server_activate(self):
        super().server_activate()
        server_ready.set()


@pytest.fixture(name='api')
async def fixture_api():
    host = 'localhost'
    port = 5000

    base_url = f'http://{host}:{port}'
    base_endpoint = '/method'

    app = Flask(__name__)

    @app.route(f'{base_endpoint}/<name>', methods=['GET'])
    def method(name):
        key = request.args.get('_key', 'response')
        return jsonify({
            key: {
                'method_name': name,
                'params': request.args
            }
        })

    server = Server(host=host, port=port, app=app, handler=Handler)

    api = Api(base_url=base_url, endpoint=base_endpoint)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(partial(
            trio.run_sync_in_worker_thread,
            server.serve_forever,
            cancellable=True
        ))
        await server_ready.wait()

        yield api

        nursery.cancel_scope.cancel()
