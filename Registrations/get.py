import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web
import json


# To get the list of registrations for the searched term
async def searchRegistrationsFn(request, db_pool:aioodbc.Pool):
    try:
        searchTerm = request.query.get("searchTerm")
        Offset = int(request.query.get("offset") or 0)
        Limit = int(request.query.get("limit") or 50)
        query = "EXEC [dbo].[RegistrationsSearch] ?,?,?"
        params = (searchTerm, Offset, Limit)

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
