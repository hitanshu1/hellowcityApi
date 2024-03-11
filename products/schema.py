
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
     
class ProductSchema(Schema):
    id=fields.Int(allow_none=True)
    name=fields.Str(required=True)
    shortName=fields.Str(allow_none=True)  
    numberCode = fields.Int(allow_none=True) 
    description=fields.Str(allow_none=True)
    vendorID=fields.Int(allow_none=True)
    adminCategoryID=fields.Int(allow_none=True)
    regularPrice = DecimalToStringField(allow_none=True)
    discountPrice = DecimalToStringField(allow_none=True)
    availableQuantity=fields.Int(allow_none=True)
    quantity=fields.Int(allow_none=True)
    type=fields.Str(allow_none=True)
    calories=fields.Int(allow_none=True)
    grams=fields.Int(allow_none=True)
    proteins=fields.Int(allow_none=True)
    fats=fields.Int(allow_none=True)
    brandID=fields.Int(allow_none=True)
    categoryID=fields.Int(allow_none=True)
    updatedBy=fields.Int(allow_none=True)
    isTakeAway=fields.Int(allow_none=True)
    isDigital=fields.Int(allow_none=True)
    imageID=fields.Int(allow_none=True)
    createdBy=fields.Int(allow_none=True)
    saleType=fields.Str(allow_none=True)
    subType=fields.Str(allow_none=True)
    status=fields.Str(allow_none=True)
    
    createdAt = DateTimeToStringField(required=True)
    updatedAt = DateTimeToStringField(allow_none=True)



