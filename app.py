import copy
import datetime
import re
import sys

import yaml

import flask
import jinja2

convoy_app = flask.Flask(__name__)
cocktail_app = flask.Flask(__name__)
ygm_app = flask.Flask(__name__)


def get_yaml(podcast):
    if podcast == 'convoy':
        resource = convoy_app.open_resource('static/convoy.yaml')
    elif podcast == 'cocktail':
        resource = convoy_app.open_resource('static/cocktail.yaml')
    elif podcast == 'ygm':
        resource = convoy_app.open_resource('static/ygm.yaml')
    elif podcast == 'kvothe':
        resource = convoy_app.open_resource('static/earless/kvothe.yaml')
    else:
        raise Exception('No yaml for {}'.format(podcast))
    return yaml.load(resource, Loader=yaml.FullLoader)


def get_eps(podcast):
    eps = podcast['episodes']
    for ep in eps:
        ep['datetime'] = datetime.datetime.strptime(
            ep['datetime'], "%Y-%m-%dT%H:%M:%S" )
    eps = {x['url'].split('_ep_')[1].split('.mp3')[0]: x for x in eps}
    for k, v in eps.items():
        v['key'] = k
    return eps


def get_convoy_data():
    podcast = get_yaml('convoy')
    years = [x['datetime'][:4] for x in podcast['episodes']]
    podcast['years'] = (min(years), max(years))
    return podcast


def get_cocktail_data():
    podcast = get_yaml('cocktail')
    years = [x['datetime'][:4] for x in podcast['episodes']]
    podcast['years'] = (min(years), max(years))
    return podcast


def get_ygm_data():
    podcast = get_yaml('ygm')
    years = [x['datetime'][:4] for x in podcast['episodes']]
    podcast['years'] = (min(years), max(years))
    return podcast


@convoy_app.route('/')
def index():
    podcast = get_convoy_data()
    return flask.render_template('index.html', podcast=podcast)


@cocktail_app.route('/')
def index():
    podcast = get_cocktail_data()
    return flask.render_template('index.html', podcast=podcast)


@ygm_app.route('/')
def index():
    podcast = get_ygm_data()
    return flask.render_template('index.html', podcast=podcast)


@convoy_app.route('/eps/')
def episodes():
    podcast = get_convoy_data()
    return flask.render_template('episodes.html', episodes=get_eps(podcast), podcast=podcast)


@cocktail_app.route('/eps/')
def episodes():
    podcast = get_cocktail_data()
    return flask.render_template('episodes.html', episodes=get_eps(podcast), podcast=podcast)


@ygm_app.route('/eps/')
def episodes():
    podcast = get_ygm_data()
    return flask.render_template('episodes.html', episodes=get_eps(podcast), podcast=podcast)


@convoy_app.route('/gallery/')
def meditative_gallery():
    podcast = get_convoy_data()
    return flask.render_template('gallery.html', episodes=get_eps(podcast), podcast=podcast)


@cocktail_app.route('/gallery/')
def meditative_gallery():
    podcast = get_cocktail_data()
    return flask.render_template('gallery.html', episodes=get_eps(podcast), podcast=podcast)


@ygm_app.route('/gallery/')
def meditative_gallery():
    podcast = get_ygm_data()
    return flask.render_template('gallery.html', episodes=get_eps(podcast), podcast=podcast)


#@cocktail_app.route('/kvothe/eps/')
#@convoy_app.route('/kvothe/eps/')
#def kvothe_episodes():
    #podcast = yaml.load(convoy_app.open_resource('static/earless/kvothe.yaml'))
    #return flask.render_template('episodes.html', episodes=get_eps(podcast), podcast=podcast)


@convoy_app.route('/playlist.html')
def playlist():
    podcast = get_convoy_data()
    return flask.render_template('playlist.html', podcast=podcast)


@cocktail_app.route('/playlist.html')
def playlist():
    podcast = get_cocktail_data()
    return flask.render_template('playlist.html', podcast=podcast)


@ygm_app.route('/playlist.html')
def playlist():
    podcast = get_ygm_data()
    return flask.render_template('playlist.html', podcast=podcast)


@convoy_app.route('/cocktails/')
def cocktails():
    podcast = get_convoy_data()
    return flask.render_template('cocktails.html', episodes=get_eps(podcast), podcast=podcast)


@cocktail_app.route('/cocktails/')
def cocktails():
    podcast = get_cocktail_data()
    return flask.render_template('cocktails.html', episodes=get_eps(podcast), podcast=podcast)


@convoy_app.route('/ep/<num>/index.html')
def episode(num):
    podcast = get_convoy_data()
    eps = get_eps(podcast)
    return flask.render_template('episode.html', episode=eps[num], podcast=podcast)


@cocktail_app.route('/ep/<num>/index.html')
def episode(num):
    podcast = get_cocktail_data()
    eps = get_eps(podcast)
    return flask.render_template('episode.html', episode=eps[num], podcast=podcast)


@ygm_app.route('/ep/<num>/index.html')
def episode(num):
    podcast = get_ygm_data()
    eps = get_eps(podcast)
    return flask.render_template('episode.html', episode=eps[num], podcast=podcast)



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


# I would just chain these decorators, but I think flask-frozen doesn't like it?
@convoy_app.route('/feed/')
def podcast_feed_legacy():
    return podcast_feed()


@convoy_app.route('/feed.xml')
@cocktail_app.route('/feed.xml')
@ygm_app.route('/feed.xml')
def podcast_feed():
    cocktail_info = get_yaml('cocktail')
    convoy_info = get_yaml('convoy')
    ygm_info = get_yaml('ygm')

    all_podcast = [convoy_info, cocktail_info, ygm_info]
    podcast = merge_podcast_info(all_podcast)
    podcast = parse_podcast_years(podcast)
    copyright_years = extract_copyright_years(podcast)
    response = flask.make_response(flask.render_template('podcast.xml',
                                     podcast=podcast,
                                     copyright_years=copyright_years))
    response.mimetype = "application/xml"
    return response


@convoy_app.route('/kvothe.xml')
@cocktail_app.route('/kvothe.xml')
@ygm_app.route('/kvothe.xml')
def kvothe_feed():
    kvothe_info = get_yaml('kvothe')
    podcast = parse_podcast_years(kvothe_info)
    copyright_years = extract_copyright_years(podcast)
    response = flask.make_response(flask.render_template('podcast.xml',
                                     podcast=podcast,
                                     copyright_years=copyright_years))
    response.mimetype = "application/xml"
    return response


@convoy_app.route('/kvothe/index.html')
@cocktail_app.route('/kvothe/index.html')
@ygm_app.route('/kvothe/index.html')
def kvothe():
    podcast = get_yaml('kvothe')
    years = [x['datetime'][:4] for x in podcast['episodes']]
    podcast['years'] = (min(years), max(years))
    return flask.render_template('index.html', podcast=podcast)


@convoy_app.route('/humans.txt')
@cocktail_app.route('/humans.txt')
def humans_txt():
    return flask.send_from_directory(convoy_app.static_folder, 'humans.txt')


@convoy_app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith('cock'):
            cocktail_app.run(debug=True)
        elif arg.startswith('con'):
            convoy_app.run(debug=True)
        elif arg.startswith('ygm'):
            ygm_app.run(debug=True)
        else:
            raise NotImplementedError(args)
    cocktail_app.run(debug=True)
