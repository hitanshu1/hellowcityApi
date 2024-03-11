
from marshmallow import Schema,fields

class DateTimeToStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat()
    
class UserSchema(Schema):
    id=fields.Int(allow_none=True)
    name=fields.Str(required=True)
    phone=fields.Int()  
    email = fields.Str(allow_none=True) 
    dateOfBirth=fields.Str(allow_none=True)
    password=fields.Str(load_only=True)
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(required=True)



