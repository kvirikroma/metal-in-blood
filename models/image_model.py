from flask_restx import fields


file_data_model = {
    "image_id":
        fields.String(
            required=True,
            description="Image id in database",
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36
        ),
    "author":
        fields.String(
            required=True,
            description="Uploader`s id in database",
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36
        ),
    "location":
        fields.String(
            required=True,
            description="Link to the image",
            example='https://youtu.be/rPiTO36udwc',
            pattern=r'\h\t\t\p\S+\/\/\S+\.\S+',
            min_length=4,
            max_length=512
        ),
    "upload_time":
        fields.DateTime(
            required=True,
            description='Date and time in iso8601 format (UTC)',
            example='2005-08-09T18:31:42.201',
            min_length=16,
            max_length=32
        )
}
