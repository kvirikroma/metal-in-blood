from flask import abort, make_response, jsonify

default_page_size = 20


def check_page(page: str):
    if not page.isdigit():
        abort(make_response(jsonify(message="Page query parameter must be integer"), 400))
