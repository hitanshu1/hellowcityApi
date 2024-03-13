import time
from marshmallow import Schema,fields

class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
    
class StuffSchema(Schema):
    id=fields.Int(allow_none=True)
    vendorID=fields.Int(required=True)
    userType=fields.Str() 
    userID=fields.Int(allow_none=True)
    active=fields.Str(allow_none=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(allow_none=True)



