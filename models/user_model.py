from flask_restplus import fields

sign_up_model = {
    "email":
        fields.String(
            required=True,
            description='User email to log in',
            example='test@mail.com',
            pattern=r'\S+@\S+\.\S+',
            min_length=5,
            max_length=256
        ),
    "login":
        fields.String(
            required=True,
            description='Unique username to find user by it',
            example='MetalHead1337',
            min_length=3,
            max_length=64
        ),
    "password":
        fields.String(
            required=True,
            description='User\'s password to log in',
            example='Qwerty123',
            min_length=8,
            max_length=64
        )
}

sign_in_model = {
    "login": sign_up_model["login"],
    "password": sign_up_model["password"]
}

full_user_model = sign_up_model.copy()
full_user_model.update({
    "user_id":
        fields.String(
            required=True,
            description='User unique id in database',
            example='d1d3ee42-731c-04d9-0eee-16d3e7a62948',
            min_length=36,
            max_length=36,
        )
})

token_model = {
    'access_token':
        fields.String(
            required=True,
            description='Token to access resources',
            example='qwerty',
        ),
    'refresh_token':
        fields.String(
            required=True,
            description='Token to refresh access resources',
            example='qwerty',
        ),
    "user_id":
        full_user_model["user_id"]
}