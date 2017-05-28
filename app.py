import copy
import datetime
import re
import yaml

import flask
import jinja2

app = flask.Flask(__name__)


def get_eps():
    podcast = yaml.load(app.open_resource('static/podcast.yaml'))
    eps = podcast['episodes']
    for ep in eps:
        ep['datetime'] = datetime.datetime.strptime(
            ep['datetime'], "%Y-%m-%dT%H:%M:%S" )
    eps = {x['url'].split('_ep_')[1].split('.mp3')[0]: x for x in eps}
    for k, v in eps.items():
        v['key'] = k
    return eps


@app.route('/')
def index():
    podcast = yaml.load(app.open_resource('static/podcast.yaml'))
    return flask.render_template('index.html', podcast=podcast)


@app.route('/eps/')
def episodes():
    return flask.render_template('episodes.html', episodes=get_eps())

@app.route('/ep/<num>')
def episode(num):
    eps = get_eps()
    return flask.render_template('episode.html', episode=eps[num])


# I would just chain these decorators, but I think flask-frozen doesn't like it?
@app.route('/feed/')
def podcast_feed_legacy():
    return podcast_feed()


@app.route('/feed.xml')
def podcast_feed():
    def extract_copyright_years(podcast):
        years = [(x['datetime']).year for x in podcast['episodes']]
        min_year = min(years)
        max_year = max(years)
        if min_year != max_year:
            return '{}-{}'.format(min_year, max_year)
        else:
            return str(max_year)

    def parse_datetime(datetime_string):
        # aka 2015-01-09T19:30:00
        return datetime.datetime(*map(int,
                                      re.split('[^\d]',
                                      datetime_string)[:-1]))

    def parse_podcast_years(podcast):
        podcast = copy.deepcopy(podcast)
        for episode in podcast['episodes']:
            episode['datetime'] = parse_datetime(episode['datetime'])
        return podcast

    podcast = yaml.load(app.open_resource('static/podcast.yaml'))
    podcast = parse_podcast_years(podcast)
    copyright_years = extract_copyright_years(podcast)
    response = flask.make_response(flask.render_template('podcast.xml',
                                     podcast=podcast,
                                     copyright_years=copyright_years))
    response.mimetype = "application/xml"
    return response


@app.route('/humans.txt')
def humans_txt():
    return flask.send_from_directory(app.static_folder, 'humans.txt')


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
