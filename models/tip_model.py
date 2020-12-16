from flask_restx import fields


tip_model = {
    "title":
        fields.String(
            required=True,
            description='Title of the tip',
            example='Slam rules',
            min_length=4,
            max_length=64
        ),
    "body":
        fields.String(
            required=True,
            description='Text of the tip',
            example='The flaming crowd pleases most musicians - this shows an extremely positive reaction to the performance',
            min_length=4,
            max_length=8192
        ),
    "tip_id":
        fields.String(
            required=True,
            description='ID of the tip',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36,
        ),
    "picture":
        fields.String(
            required=False,
            description='',
            example='https://i.imgur.com/69khNTK.jpg',
            pattern=r'http\S+//\S+\.\S+',
            min_length=4,
            max_length=512
        )
}
