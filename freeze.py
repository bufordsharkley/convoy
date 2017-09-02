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
    info = app.cocktail_info
else:
    freezer = Freezer(app.app)
    info = app.convoy_info


@freezer.register_generator
def episode():
    for ep in app.get_eps(info):
        yield {'num': ep}

freezer.freeze()
