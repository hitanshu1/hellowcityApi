import time
from marshmallow import Schema,fields

class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
    
class OfferSchema(Schema):
    id=fields.Int(allow_none=True)
    title=fields.Str(required=True)
    description = fields.Str(required=True)
    vendorID=fields.Int(required=True)
    type=fields.Str() 
    status=fields.Str(allow_none=True)
    startDate=DateTimeToStringField(allow_none=True)
    endDate=DateTimeToStringField(allow_none=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(allow_none=True)



