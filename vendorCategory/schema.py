import time
from marshmallow import Schema,fields

class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
    
class VendorCategorySchema(Schema):
    id=fields.Int(allow_none=True)
    name=fields.Str(required=True)
    status=fields.Str(allow_none=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(required=True)



