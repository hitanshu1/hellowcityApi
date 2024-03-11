import aioodbc
from aiohttp import web,web_request
from access_token import AccessToken
from apiResponse import ApiResponse

@AccessToken.token_required
async def deleteProductCategory(request, db_pool:aioodbc.Pool):
    try:
        data = await request.post()
        id = data.get('id')

        if id is None:
            return web.json_response({"success": False, "data": {}, "message": "Record doesn't exist"})
        else:
            query = "DELETE FROM productCategory WHERE id = ?;"
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query, id)
                    rowCount = cursor.rowcount
                    if rowCount == -1:
                        return ApiResponse.message(False,{},"Record doesn't exist")
                    else:
                        await cnxn.commit()
                        return ApiResponse.message(True,{},"Successfully deleted")
    except Exception as e:
        return ApiResponse.message(False,{},str(e))