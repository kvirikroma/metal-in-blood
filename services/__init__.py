from uuid import UUID

from flask import abort, make_response, jsonify


default_page_size = 20


def check_page(request):
    page = request.args.get("page")
    if not page or not page.isdigit():
        abort(make_response(jsonify(message="Page query parameter must exist and be integer"), 400))
    page = int(page) - 1
    if page < 0:
        abort(make_response(jsonify(message="Page query parameter must be >= 1"), 400))
    if page >= 2147483647:
        abort(make_response(jsonify(message="Page query parameter is too large"), 400))
    return page


def check_uuid(value: str):
    try:
        UUID(value)
        return True
    except ValueError:
        abort(make_response(jsonify(message="Incorrect id parameter (must match UUID v4)"), 400))
    except TypeError:
        abort(make_response(jsonify(message="Cannot find id parameter of correct type (must appear once in query)"), 400))
