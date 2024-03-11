import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken

# To add a vendor to the database
@AccessToken.token_required
async def addVendor(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a vendor from the database
@AccessToken.token_required
async def updateVendor(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an vendor to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.json()
        values = (data.get("name"), data.get("authorID"), data.get("categoryID"), data.get("fcmToken"), data.get('sectionId'),
          data.get("description"), data.get("phone"), data.get("addressID"), data.get("photoID"), data.get("backgroundImageID"),
          data.get('logoID'), data.get('orderCounter'), data.get('hidePhotos'), data.get('dineInActive'),
          data.get('bookAvailable'), data.get('deliveryChargeID'), data.get('workingHoursID'),
          data.get('vendorType'), data.get('activeStatus'), data.get('taxInfoID'), data.get('kyCDetailsID'),
          data.get('upiInfoID'), data.get('bookingStatus'), data.get('status'))

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE vendor SET "
        else:
            query = "INSERT INTO vendor "

        if toAdd:
            query += "(name, authorID, categoryID, fcmToken, sectionId, description, phone, addressID, photoID, backgroundImageID, logoID, orderCounter, hidePhotos, dineInActive, bookAvailable, deliveryChargeID, workingHoursID, vendorType, activeStatus, taxInfoID, kyCDetailsID, upiInfoID, bookingStatus, status) "
            query += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        else:
            query += "name=?, authorID=?, categoryID=?, fcmToken=?, sectionId=?, description=?, phone=?, addressID=?, photoID=?, backgroundImageID=?, logoID=?, orderCounter=?, hidePhotos=?, dineInActive=?, bookAvailable=?, deliveryChargeID=?, workingHoursID=?, vendorType=?, activeStatus=?, taxInfoID=?, kyCDetailsID=?, upiInfoID=?, bookingStatus=?, status=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
        
        success_response = {
            "message": f"{'added sccessfully' if toAdd else 'updated successfully'}!"
        }
        return web.json_response(success_response, status=200)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)