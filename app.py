import copy
import datetime
import re
import yaml

import flask
import jinja2

app = flask.Flask(__name__)


@app.route('/')
def index():
    podcast = yaml.load(app.open_resource('static/podcast.yaml'))
    return flask.render_template('index.html', podcast=podcast)


@app.route('/feed/')
def podcast_feed():
    def extract_copyright_years(podcast):
        years = [(x['datetime']).year for x in podcast['episodes']]
        min_year = min(years)
        max_year = max(years)
        if min_year != max_year:
            return str(max_year)
        else:
            return str(max_year)

    def parse_datetime(datetime_string):
        # aka 2015-01-09T19:30:00
        return datetime.datetime(*map(int, re.split('[^\d]', datetime_string)[:-1]))

    def parse_podcast_years(podcast):
        podcast = copy.deepcopy(podcast)
        for episode in podcast['episodes']:
            episode['datetime'] = parse_datetime(episode['datetime'])
        return podcast

    podcast = yaml.load(app.open_resource('static/podcast.yaml'))
    podcast = parse_podcast_years(podcast)
    copyright_years = extract_copyright_years(podcast)
    template = jinja2.Template("""\
<?xml version="1.0" encoding="UTF-8" ?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>{{ podcast.title }}</title>
<description>{{ podcast.description }}</description>
<link>{{ podcast.website }}</link>
<language>en-us</language>
<itunes:subtitle>{{ podcast.description }}</itunes:subtitle>
<itunes:author>{{ podcast.host }}</itunes:author>
<itunes:summary>{{ podcast['long description'] }}</itunes:summary>
<itunes:image href="{{ podcast.logo }}"/>
<itunes:category text="{{ podcast['itunes category'] }}" />
<itunes:explicit>{{ podcast['itunes explicit'] }}</itunes:explicit>
<image>
    <url>{{ podcast.logo }}</url>
    <title>{{ podcast.title }}</title>
    <link>{{ podcast.website }}</link>
</image>
<copyright>Copyright {{ copyright_years }}, {{ podcast.title}} Family</copyright>
{% for episode in podcast.episodes -%}
<item>
    <title>{{ episode.title }}</title>
    <description>{{ episode.description }}</description>
    <itunes:summary>{{ episode.description }}</itunes:summary>
    <link>{{ podcast.website }}</link>
    <guid isPermaLink="false">ep{{ loop.index }}</guid>
    <pubDate>{{ episode.datetime.strftime("%a, %-d %b %Y %H:%M:%S +0000")}}</pubDate>
    <enclosure url="{{ episode.url }}" length="{{ episode['audio size'] }}" type="audio/mpeg" />
</item>
{% endfor -%}
</channel>
</rss>

""")

    text = template.render(podcast=podcast, copyright_years=copyright_years)
    response = flask.make_response(text)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/humans.txt')
def humans_txt():
    return flask.send_from_directory(app.static_folder, 'humans.txt')


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
