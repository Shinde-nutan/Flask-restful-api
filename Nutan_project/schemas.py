from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1), error_messages={"required": "Title is required"})
    description = fields.Str(required=True, validate=validate.Length(min=1), error_messages={"required": "Description is required"})
    director = fields.Str()
    genre = fields.Str()
    release_date = fields.Date(required=True, format='%Y-%m-%d')
    average_rating = fields.Float(required=True, validate=validate.Range(min=1, max=10), error_messages={"required": "Average rating is required"})
    ticket_price = fields.Float()
    cast = fields.Str()