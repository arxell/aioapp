from app.views import index, test_aiojobs, test_sse, test_websocket


def setup_routes(app):
    app.router.add_route('GET', '/index', index.handler)
    app.router.add_route('GET', '/test/aiojobs', test_aiojobs.view)
    app.router.add_route('GET', '/test/sse', test_sse.handler)
    app.router.add_route('GET', '/test/websocket', test_websocket.handler)
