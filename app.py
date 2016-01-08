import datetime

from flask import Flask, render_template, abort, redirect, url_for, request, send_from_directory
from jinja2 import TemplateNotFound

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feed/')
def podcast_feed():
    return send_from_directory(app.static_folder, 'podcast.xml')


@app.route('/<path:path>/')
def subpage(path):
    try:
        return render_template(path + '.html')
    except TemplateNotFound:
        abort(404)


@app.route('/hackers.txt')
def hackers():
    return 'site has been hacked at time: {}'.format(datetime.datetime.now())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
