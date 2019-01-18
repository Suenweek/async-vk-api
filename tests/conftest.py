from functools import partial

import trio
import pytest
from flask import Flask, jsonify, request
from werkzeug.serving import BaseWSGIServer, WSGIRequestHandler

from async_vk_api.api import Api, make_session


server_ready = trio.Event()


class Handler(WSGIRequestHandler):

    protocol_version = 'HTTP/1.1'


class Server(BaseWSGIServer):

    def server_activate(self):
        super().server_activate()
        server_ready.set()


@pytest.fixture(name='api')
async def fixture_api(nursery):
    host = 'localhost'
    port = 5000

    base_location = f'http://{host}:{port}'
    endpoint = '/method'

    app = Flask(__name__)

    @app.route(f'{endpoint}/<name>', methods=['GET'])
    def method(name):
        key = request.args.get('_key', 'response')
        return jsonify({
            key: {
                'method_name': name,
                'params': request.args
            }
        })

    server = Server(host=host, port=port, app=app, handler=Handler)

    session = make_session(base_location=base_location,
                           endpoint=endpoint)

    api = Api(access_token='test_access_token',
              version='test_version',
              session=session)

    nursery.start_soon(partial(
        trio.run_sync_in_worker_thread,
        server.serve_forever,
        cancellable=True
    ))
    await server_ready.wait()

    yield api
