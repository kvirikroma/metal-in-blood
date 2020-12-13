import os

from flask import Flask, render_template, send_from_directory, redirect, request

from models.user_model import Language
from . import vocabulary


def bind_frontend_pages(app: Flask):
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static/metal-in-blood/'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route("/", methods=["GET"])
    def index():
        return redirect("index.html")

    @app.route("/<string:page_name>.html", methods=["GET"])
    def page(page_name: str):
        lang_raw = request.args.get("lang")
        try:
            if not lang_raw:
                raise KeyError
            lang = Language[lang_raw]
        except KeyError:
            lang = Language.en
        print(lang)
        return render_template(page_name + ".html", **(vocabulary.en if lang == Language.en else vocabulary.ua))
