import optparse

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
    else:
        freezer = Freezer(app.convoy_app)
        info = app.get_yaml('convoy')
        app.convoy_app.config['FREEZER_DESTINATION'] = 'convoy_build'

    check_url_validity(info)

    @freezer.register_generator
    def episode():
        for ep in app.get_eps(info):
            yield {'num': ep}

    freezer.freeze()

if __name__ == "__main__":
    main()
