import json
import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib
from access_token import AccessToken
from apiResponse import ApiResponse
from appSettings.schema import AppSettingsSchema

async def getAppSettings(request:web_request.Request, db_pool:aioodbc.Pool):
    try:   
        query = f"SELECT * FROM appSettings WHERE id = 1"
        async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query)
                    row = await cursor.fetchone()
                    columns = [column[0] for column in cursor.description]
                    if row:
                        item_dic = dict(zip(columns, row))
                        appSettingsSchema = AppSettingsSchema()
                        try:
                            vendor_data = appSettingsSchema.load(item_dic)
                            serialized_data = appSettingsSchema.dump(vendor_data)
                            return ApiResponse.message(True, serialized_data)
                        except Exception as e:
                            return ApiResponse.message(False, {}, str(e))
                    else:
                        return ApiResponse.message(False, {}, "No result found")


    except Exception as e:
        return ApiResponse.message(False,{},str(e))