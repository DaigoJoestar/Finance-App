from marshmallow import Schema, fields, validate, ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError("Amount must be positive.")

class UserCreateSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(['viewer', 'analyst', 'admin']))
    active = fields.Bool()

class UserUpdateSchema(Schema):
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(['viewer', 'analyst', 'admin']))
    active = fields.Bool()

class RecordSchema(Schema):
    amount = fields.Float(required=True, validate=validate_positive)
    type = fields.Str(required=True, validate=validate.OneOf(['income', 'expense']))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    date = fields.Date(required=True, format='%Y-%m-%d')
    description = fields.Str()
    user_id= fields.Integer(required=False)