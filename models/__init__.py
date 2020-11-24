from flask_restx import fields


pages_count_model = fields.Integer(
    required=False,
    description="Total count of pages in the resource",
    example=1,
    min=0
)
