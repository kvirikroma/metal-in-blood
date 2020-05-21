from flask import Flask, render_template


def custom_abort_page(message: str, code: int):
    return render_template("error_page.html", code=str(code), text=message)


def bind_error_pages(app: Flask):
    @app.errorhandler(500)
    def error500(err):
        return custom_abort_page(err.description, 500), 500

    @app.errorhandler(409)
    def error409(err):
        return custom_abort_page(err.description, 409), 409

    @app.errorhandler(404)
    def error404(err):
        return custom_abort_page(err.description, 404), 404

    @app.errorhandler(403)
    def error403(err):
        return custom_abort_page(err.description, 403), 403

    @app.errorhandler(401)
    def error401(err):
        return custom_abort_page(err.description, 400), 401

    @app.errorhandler(400)
    def error400(err):
        return custom_abort_page(err.description, 400), 400
