#import pathlib
import optparse
import os

from flask_frozen import Freezer
import requests

import app


def check_url_validity(info):
    for ep in info['episodes']:
        url = ep['url']
        print(ep['url'])
        r = requests.head(url)
        r.raise_for_status()
        yaml_size = int(ep['audio size'])
        head_size = int(r.headers['Content-Length'])
        if yaml_size != head_size:
            print('Discrepancy: {} vs {}'.format(yaml_size, head_size))


def main():
    parser = optparse.OptionParser(usage="usage: %prog [options] podcast")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Must specify podcast")

    podcast = args[0].strip().lower()

    if podcast == 'cocktail':
        freezer = Freezer(app.cocktail_app)
        info = app.get_yaml('cocktail')
        app.cocktail_app.config['FREEZER_DESTINATION'] = 'cocktail_build'
    elif podcast == 'ygm':
        freezer = Freezer(app.ygm_app)
        info = app.get_yaml('ygm')
        app.ygm_app.config['FREEZER_DESTINATION'] = 'ygm_build'
    elif podcast == 'jumper':
        freezer = Freezer(app.jumper_app)
        info = app.get_yaml('jumper')
        app.jumper_app.config['FREEZER_DESTINATION'] = 'jumper_build'
    else:
        freezer = Freezer(app.convoy_app)
        info = app.get_yaml('convoy')
        app.convoy_app.config['FREEZER_DESTINATION'] = 'convoy_build'

    check_url_validity(info)

    @freezer.register_generator
    def episode():
        for ep in app.get_eps(info):
            yield {'num': ep}

    @freezer.register_generator
    def prescreen():
        for title, hashtag in app.get_prescreens(info):
            yield {'hashtag': hashtag}

    if podcast == 'ygm':
        # register every single file in classic site:
        @freezer.register_generator
        def ygm_classic_site():
            for dirpath, _, filenames in os.walk('static/ygm_site'):
                for fname in filenames:
                    # Uhhh, we're stuck with 2.7... ?
                    # The correct way we'll avoid for now:
                    #path = pathlib.Path(dirpath, fname)
                    #path = pathlib.Path(*path.parts[2:])
                    try:
                        ddirpath = dirpath.split('/', 2)[2]
                    except IndexError:
                        ddirpath = ''
                    path = os.path.join(ddirpath, fname)
                    yield {'path': path}

    freezer.freeze()

if __name__ == "__main__":
    main()
