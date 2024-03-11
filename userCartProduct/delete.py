import aioodbc
from aiohttp import web,web_request
from access_token import AccessToken
from apiResponse import ApiResponse

@AccessToken.token_required
async def deleteCartProduct(request, db_pool:aioodbc.Pool):
    try:
        data = await request.json()
        id = data.get('id')

        if id is None:
            return web.json_response({"success": False, "data": {}, "message": "Record doesn't exist"})
        else:
            query = "DELETE FROM userCartProduct WHERE id = ?;"
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
    
@AccessToken.token_required
async def deleteAllCartProduct(request, db_pool:aioodbc.Pool):
    try:
        data = await request.post()
        userID = data.get('userID')

        if userID is None:
            return web.json_response({"success": False, "data": {}, "message": "Record doesn't exist"})
        else:
            query = "DELETE FROM userCartProduct WHERE userID = ?;"
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query, userID)
                    rowCount = cursor.rowcount
                    if rowCount == -1:
                        return ApiResponse.message(False,{},"Record doesn't exist")
                    else:
                        await cnxn.commit()
                        return ApiResponse.message(True,{},"Successfully deleted")
    except Exception as e:
        return ApiResponse.message(False,{},str(e))