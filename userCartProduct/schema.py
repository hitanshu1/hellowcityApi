import time
from marshmallow import Schema,fields

class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
    
class CartProductSchema(Schema):
    id=fields.Int(required=True)
    userID=fields.Int(allow_none=True)
    vendorID = fields.Int(allow_none=True)
    productID=fields.Int(allow_none=True)
    quantity=fields.Int(allow_none=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(allow_none=True)



