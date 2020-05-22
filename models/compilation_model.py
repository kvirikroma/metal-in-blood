from flask_restplus import fields


album_model = {
    "author":
        fields.String(
            required=True,
            description='Author of an album',
            example="Erra",
            min_length=2,
            max_length=64
        ),
    "title":
        fields.String(
            required=True,
            description='Title of an album',
            example="Neon",
            min_length=2,
            max_length=64
        ),
    "picture":
        fields.String(
            required=False,
            description='Link to the picture',
            example='https://metalarea.org/images/audiocovers/2018_Aug/acov_tid309143.jpg',
            pattern=r'\h\t\t\p\S+\/\/\S+\.\S+',
            min_length=4,
            max_length=512
        )
}


yt_compilation_model = {
    "channel":
        fields.String(
            required=True,
            description='Channel that posted the video',
            example="Ace Guitar",
            min_length=2,
            max_length=64
        ),
    "video_name":
        fields.String(
            required=True,
            description='Name of the video',
            example="1 Hour Prog Metalcore Mix",
            min_length=2,
            max_length=64
        ),
    "link":
        fields.String(
            required=False,
            description='Link to the video',
            example='https://youtu.be/rPiTO36udwc',
            pattern=r'\h\t\t\p\S+\/\/\S+\.\S+',
            min_length=4,
            max_length=512
        )
}
