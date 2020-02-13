import optparse

from flask_frozen import Freezer

import app

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
    FREEZER_DESTINATION = 'convoy_build'
    app.convoy_app.config['FREEZER_DESTINATION'] = 'convoy_build'


@freezer.register_generator
def episode():
    for ep in app.get_eps(info):
        yield {'num': ep}

freezer.freeze()
