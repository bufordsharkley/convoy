import datetime

from flask import Flask, render_template, abort, redirect, url_for, request, send_from_directory
from jinja2 import TemplateNotFound

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feed/')
def podcast_feed():
    response = send_from_directory(app.static_folder, 'podcast.xml')
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/humans.txt')
def humans_txt():
    return send_from_directory(app.static_folder, 'humans.txt')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
