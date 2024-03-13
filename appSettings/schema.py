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
    
class AppSettingsSchema(Schema):
    id=fields.Int(allow_none=True)
    subscription=fields.Int(allow_none=True) 
    advertisement=fields.Int(allow_none=True) 
    active=fields.Int(allow_none=True) 
    detailsOnVendorPrint=fields.Int(allow_none=True) 
    showPhoneOnPrint=fields.Int(allow_none=True) 
    version=fields.Str(allow_none=True) 
    decimalPlace=fields.Int(allow_none=True) 
    adminCommission=fields.Int(allow_none=True) 
    macDownloadUrl=fields.Str(allow_none=True) 
    windowsDownloadUrl=fields.Str(allow_none=True) 
    androidDownloadUrl=fields.Str(allow_none=True) 
    iosDownloadUrl=fields.Str(allow_none=True) 
    currencySymbol=fields.Str(allow_none=True) 
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(allow_none=True)



