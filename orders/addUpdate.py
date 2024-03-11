import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken

# To add a vendor to the database
@AccessToken.token_required
async def addOrder(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a vendor from the database
@AccessToken.token_required
async def updateOrder(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an vendor to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.post()
        values = (data.get("bag"), data.get("vendorID"), data.get("stuffID"), data.get("createdBy"), data.get('orderType'),
          data.get("grandTotal"), data.get("vendorTotal"), data.get("addressID"), data.get("userID"), data.get("cabinID"),
          data.get('overAllDiscount'), data.get('priceDiscount'), data.get('paymentMethodID'), data.get('gstAmount'),
          data.get('deliveryCharge'), data.get('serviceTax'), data.get('driverID'),
          data.get('offerID'), data.get('tipValue'), data.get('adminCommission'), data.get('adminCommissionType'),
          data.get('takeAway'), data.get('courierCompanyName'), data.get('courierTrackingId'),data.get('scheduleTime'),
          data.get('estimatedTimeToPrepare'),data.get('deliveryDate'),data.get('paymentStatus'),data.get('status'),
          data.get('updatedAt'))

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE orders SET "
        else:
            query = "INSERT INTO orders "

        if toAdd:
            query += "(bag, vendorID, stuffID, createdBy, orderType, grandTotal, vendorTotal, addressID, userID, cabinID, overAllDiscount, priceDiscount, paymentMethodID, gstAmount, deliveryCharge, serviceTax, driverID, offerID, tipValue, adminCommission, adminCommissionType, takeAway, courierCompanyName,courierTrackingId, scheduleTime,estimatedTimeToPrepare,deliveryDate,paymentStatus,status,updatedAt) "
            query += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?) "
        else:
            query += "bag=?, vendorID=?, stuffID=?, createdBy=?, orderType=?, grandTotal=?, vendorTotal=?, addressID=?, userID=?, cabinID=?, overAllDiscount=?, priceDiscount=?, paymentMethodID=?, gstAmount=?, deliveryCharge=?, serviceTax=?, driverID=?, offerID=?,tipValue=?, adminCommission=?, adminCommissionType=?, takeAway=?, courierCompanyName=?, courierTrackingId=?, scheduleTime=?,estimatedTimeToPrepare=?,deliveryDate=?,paymentStatus=?,status=?,updatedAt=? WHERE id=?"
        
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