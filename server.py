from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/metal-in-blood/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/<string:page_name>.html", methods=["GET"])
def page(page_name: str):
    return render_template(page_name + ".html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
