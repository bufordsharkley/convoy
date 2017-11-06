import copy
import datetime
import re
import sys

import yaml

import flask
import jinja2

convoy_app = flask.Flask(__name__)

cocktail_app = flask.Flask(__name__)


cocktail_info = yaml.load(convoy_app.open_resource('static/cocktail.yaml'))
convoy_info = yaml.load(convoy_app.open_resource('static/convoy.yaml'))


def get_eps(podcast):
    eps = podcast['episodes']
    for ep in eps:
        ep['datetime'] = datetime.datetime.strptime(
            ep['datetime'], "%Y-%m-%dT%H:%M:%S" )
    eps = {x['url'].split('_ep_')[1].split('.mp3')[0]: x for x in eps}
    for k, v in eps.items():
        v['key'] = k
    return eps


@convoy_app.route('/')
def index():
    podcast = yaml.load(convoy_app.open_resource('static/convoy.yaml'))
    return flask.render_template('index.html', podcast=podcast)


@cocktail_app.route('/')
def index():
    podcast = yaml.load(convoy_app.open_resource('static/cocktail.yaml'))
    return flask.render_template('index.html', podcast=podcast)


@cocktail_app.route('/eps/')
def episodes():
    podcast = yaml.load(convoy_app.open_resource('static/cocktail.yaml'))
    return flask.render_template('episodes.html', episodes=get_eps(podcast), podcast=podcast)


@convoy_app.route('/cocktails/')
def cocktails():
    podcast = yaml.load(convoy_app.open_resource('static/convoy.yaml'))
    return flask.render_template('cocktails.html', episodes=get_eps(podcast), podcast=podcast)


@cocktail_app.route('/cocktails/')
def cocktails():
    podcast = yaml.load(convoy_app.open_resource('static/cocktail.yaml'))
    return flask.render_template('cocktails.html', episodes=get_eps(podcast), podcast=podcast)

@convoy_app.route('/eps/')
def episodes():
    podcast = yaml.load(convoy_app.open_resource('static/convoy.yaml'))
    return flask.render_template('episodes.html', episodes=get_eps(podcast), podcast=podcast)


@convoy_app.route('/ep/<num>')
def episode(num):
    podcast = yaml.load(convoy_app.open_resource('static/convoy.yaml'))
    eps = get_eps(podcast)
    return flask.render_template('episode.html', episode=eps[num], podcast=podcast)


@cocktail_app.route('/ep/<num>')
def episode(num):
    podcast = yaml.load(convoy_app.open_resource('static/cocktail.yaml'))
    eps = get_eps(podcast)
    return flask.render_template('episode.html', episode=eps[num], podcast=podcast)


# I would just chain these decorators, but I think flask-frozen doesn't like it?
@convoy_app.route('/feed/')
def podcast_feed_legacy():
    return podcast_feed()


@convoy_app.route('/feed.xml')
@cocktail_app.route('/feed.xml')
def podcast_feed():
    cocktail_info = yaml.load(cocktail_app.open_resource('static/cocktail.yaml'))
    convoy_info = yaml.load(convoy_app.open_resource('static/convoy.yaml'))
    def extract_copyright_years(podcast):
        years = [(x['datetime']).year for x in podcast['episodes']]
        if not years:
            return '1994-1998'
        min_year = min(years)
        max_year = max(years)
        if min_year != max_year:
            return '{}-{}'.format(min_year, max_year)
        else:
            return str(max_year)

    def parse_datetime(datetime_string):
        # aka 2015-01-09T19:30:00
        if isinstance(datetime_string, datetime.datetime):
            return datetime_string
        return datetime.datetime(*map(int,
                                      re.split('[^\d]',
                                      datetime_string)[:-1]))

    def parse_podcast_years(podcast):
        podcast = copy.deepcopy(podcast)
        for episode in podcast['episodes']:
            episode['datetime'] = parse_datetime(episode['datetime'])
        return podcast

    def merge_podcast_info(all_info):
        resp = {}
        for info in all_info:
            for k, v in info.items():
                if k == 'episodes' and 'episodes' in resp:
                    resp[k] = resp[k] + v
                else:
                    resp[k] = v
        return resp

    all_podcast = [convoy_info, cocktail_info]
    podcast = merge_podcast_info(all_podcast)
    podcast = parse_podcast_years(podcast)
    copyright_years = extract_copyright_years(podcast)
    response = flask.make_response(flask.render_template('podcast.xml',
                                     podcast=podcast,
                                     copyright_years=copyright_years))
    response.mimetype = "application/xml"
    return response


@convoy_app.route('/humans.txt')
@cocktail_app.route('/humans.txt')
def humans_txt():
    return flask.send_from_directory(convoy_app.static_folder, 'humans.txt')


@convoy_app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


if __name__ == '__main__':
    if len(sys.argv) > 2:
        convoy_app.run(debug=True)
    cocktail_app.run(debug=True)
