
from aiohttp import web


class ApiResponse:
    def message(success:bool,result,message=''):
        response_data = {
                    "status": 1 if success else 0,
                    "data": result,
                    "message": message
                        }
        return web.json_response(response_data)