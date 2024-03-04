import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web
import json


# To login a user for the given email & password
async def loginFn(request, db_pool:aioodbc.Pool):
    try:
        id = request.query.get("id")
        password = request.query.get("password")
        query = "EXEC [dbo].[login] ?,?"
        params = (id, password)
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, params)
                rows = await cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                result_json = json.dumps(result, indent=4, default=str)

        return web.Response(text=result_json, content_type="application/json")
    except Exception as e:
        return await mssqlExceptionManager(e)
