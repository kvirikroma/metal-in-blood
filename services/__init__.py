from flask import abort, make_response, jsonify

default_page_size = 20


def check_page(request):
    page = request.args.get("page")
    if not page or not page.isdigit():
        abort(make_response(jsonify(message="Page query parameter must exist and be integer"), 400))
    page = int(page) - 1
    if page < 0:
        abort(make_response(jsonify(message="Page query parameter must be >= 1"), 400))
    return page
