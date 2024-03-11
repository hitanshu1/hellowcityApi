
from marshmallow import Schema,fields

class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
class DecimalToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)
    
class OrderSchema(Schema):
    id=fields.Int(allow_none=True)
    bag=fields.Str(allow_none=True)
    vendorID=fields.Int(allow_none=True)  
    stuffID=fields.Int(allow_none=True)  
    createdBy=fields.Int(allow_none=True)  
    orderType=fields.Str(allow_none=True)  
    grandTotal=DecimalToStringField(allow_none=True) 
    vendorTotal=DecimalToStringField(allow_none=True)
    addressID=fields.Int(allow_none=True)  
    userID=fields.Int(allow_none=True)  
    cabinID=fields.Int(allow_none=True)  
    overAllDiscount=DecimalToStringField(allow_none=True)  
    priceDiscount=DecimalToStringField(allow_none=True) 
    paymentMethodID=fields.Int(allow_none=True)  
    gstAmount=DecimalToStringField(allow_none=True) 
    deliveryCharge=DecimalToStringField(allow_none=True)
    serviceTax=DecimalToStringField(allow_none=True)
    driverID=fields.Int(allow_none=True) 
    offerID=fields.Int(allow_none=True) 
    tipValue=DecimalToStringField(allow_none=True)
    adminCommission=DecimalToStringField(allow_none=True)
    adminCommissionType=fields.Str(allow_none=True) 
    takeAway=fields.Int(allow_none=True) 
    courierCompanyName=fields.Str(allow_none=True) 
    courierTrackingId=fields.Str(allow_none=True) 
    scheduleTime=fields.Int(allow_none=True) 
    estimatedTimeToPrepare=fields.Int(allow_none=True)  
    deliveryDate = DateTimeToStringField(allow_none=True)
    dateOfBirth=fields.Str(allow_none=True)
    paymentStatus=fields.Str(allow_none=True)
    status=fields.Str(allow_none=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(allow_none=True)



