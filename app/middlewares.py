async def authentication_handler(app, handler):
    async def middleware(request):
        # TODO: (@ivan.elfimov) add actual logic
        request['user_id'] = 123
        response = await handler(request)
        return response

    return middleware
