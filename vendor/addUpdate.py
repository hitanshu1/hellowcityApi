import json
import os
import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken
from apiResponse import ApiResponse
from vendor.vendorImages import uploadVendorImages
from vendor.vendorLogo import uploadVendorLogo

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
        bodyData = await request.post()
        images=bodyData.getall('images')
        logo=bodyData.get('logo')
        data_str =bodyData.get('data').decode('utf-8')
        data=json.loads(data_str)
        
        values = (data.get("name"), data.get("authorID"), data.get("categoryID"), data.get("fcmToken"), 
                  data.get('sectionId'),
          data.get("description"), data.get("phone"),
            # data.get("addressID"), data.get("photoID"), data.get("backgroundImageID"),
        #   data.get('logoID'),
            data.get('orderCounter'), data.get('hidePhotos'), data.get('dineInActive'),
          data.get('bookAvailable'),
            # data.get('deliveryChargeID'), data.get('workingHoursID'),
          data.get('vendorType'), data.get('activeStatus'),
        #     data.get('taxInfoID'), data.get('kyCDetailsID'),
           data.get('upiID'), 
          data.get('bookingStatus'), data.get('status'))

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE vendor SET "
        else:
            query = "INSERT INTO vendor "

        if toAdd:
            query += "(name, authorID, categoryID, fcmToken, sectionId, description, phone, orderCounter, hidePhotos, dineInActive, bookAvailable,  vendorType, activeStatus, upiID, bookingStatus, status) "
            query += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?) "
        else:
            query += "name=?, authorID=?, categoryID=?, fcmToken=?, sectionId=?, description=?, phone=?, orderCounter=?, hidePhotos=?, dineInActive=?, bookAvailable=?, vendorType=?, activeStatus=?, taxInfoID=?, kyCDetailsID=?, upiInfoID=?,upiID=?, bookingStatus=?, status=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
                await cursor.execute("SELECT @@IDENTITY")
                row = await cursor.fetchone()
                if row:
                    inserted_id = row[0]
                    images = list(filter(lambda x: x != '', images))
                    if images is not None:
                        
                        await uploadVendorImages(files=images,vendorID=inserted_id,db_pool=db_pool)
                    if logo is not None:
                        await uploadVendorLogo(file=logo,vendorID=inserted_id,db_pool=db_pool)
      
        
        success_response = {
            "message": f"{'added sccessfully' if toAdd else 'updated successfully'}!"
        }
        raise ApiResponse.message(True,{},success_response)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return ApiResponse.message(False,{},error_message)
    