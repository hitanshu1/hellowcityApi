import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib
from access_token import AccessToken

from extension.datetimeEx import to_datetime

# To add a offer to the database
@AccessToken.token_required
async def addAppSetting(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a offer from the database
@AccessToken.token_required
async def updateAppSetting(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an offer to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):
    

    try:    
        data = await request.post()
        print(data)
      
        values = (data.get("subscription"), data.get("advertisement"), data.get("active"), data.get("detailsOnVendorPrint"),
                  data.get("showPhoneOnPrint"),data.get("version"),data.get("decimalPlace"),data.get("adminCommission"),
                  data.get("macDownloadUrl"),data.get("windowsDownloadUrl"),data.get("androidDownloadUrl"),data.get("iosDownloadUrl"),
                  data.get("currencySymbol"),
                  )
        print(values)
        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE appSettings SET "
        else:
            query = "INSERT INTO appSettings "

        if toAdd:
            
            query += "(subscription, advertisement, active, detailsOnVendorPrint,showPhoneOnPrint, version, decimalPlace,adminCommission,macDownloadUrl,windowsDownloadUrl,androidDownloadUrl,iosDownloadUrl,currencySymbol) "
            query += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        else:
            query += "subscription=?, advertisement=?, active=?, detailsOnVendorPrint=?, showPhoneOnPrint=?, version=?, decimalPlace=?, adminCommission=?,macDownloadUrl=?,windowsDownloadUrl=?,androidDownloadUrl=?,iosDownloadUrl=?,currencySymbol=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
        
        success_response = {
            "message": f"{'Added sccessfully' if toAdd else 'Updated successfully'}!"
        }
        return web.json_response(success_response, status=200)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)