from flask import abort

default_page_size = 20


def check_page(page: str):
    if not page.isdigit():
        abort(400, "Page query parameter must be integer")
