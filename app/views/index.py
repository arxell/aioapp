from aiohttp.web import Response


def get_response():
    d = """
        <html>
            <head>
            </head>
            <body>
            HELLO
            </body>
        </html>
    """
    return Response(text=d, content_type='text/html')


async def handler(request):
    return get_response()
