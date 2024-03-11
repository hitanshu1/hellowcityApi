import time
from marshmallow import Schema,fields

# class MillisecondsSinceEpoch(fields.Field):
#     def _serialize(self, value, attr, obj, **kwargs):
#         if value is None:
#             return None
#         return int(time.mktime(value.timetuple()) * 1000)
class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
    
class VendorSchema(Schema):
    id=fields.Int(allow_none=True)
    name=fields.Str(required=True)
    description = fields.Str(required=True)
    phone=fields.Int()  
    vendorType=fields.Str() 
    workingHoursID = fields.Int(allow_none=True),
    bookAvailable = fields.Int(allow_none=True)
    backgroundImageID=fields.Int(allow_none=True),
    dineInActive=fields.Int(allow_none=True)
    orderCounter=fields.Int(allow_none=True)
    backgroundImageID=fields.Int(allow_none=True)
    deliveryChargeID=fields.Int(allow_none=True)
    activeStatus=fields.Str(allow_none=True)
    authorID=fields.Int(allow_none=True)
    kyCDetailsID=fields.Int(allow_none=True)
    photoID=fields.Int(allow_none=True)
    fcmToken=fields.Str(allow_none=True)
    categoryID=fields.Int(allow_none=True)
    hidePhotos=fields.Int(allow_none=True)
    logoID=fields.Int(allow_none=True)
    upiInfoID=fields.Int(allow_none=True)
    taxInfoID=fields.Int(allow_none=True)
    status=fields.Str(allow_none=True)
    sectionId=fields.Int(allow_none=True)
    bookingStatus=fields.Str(allow_none=True)
    workingHoursID=fields.Int(allow_none=True)
    addressID=fields.Int(allow_none=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(required=True)



