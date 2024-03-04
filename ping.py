from aiohttp import web
import aioodbc


# To check if the connection is available goes here
async def pingFn(request, db_pool:aioodbc.Pool):
    response_data = {"message": "API version 2.0.3 is running successfully!"}
    return web.json_response(response_data, status=200)
