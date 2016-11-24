from flask_frozen import Freezer

import app

freezer = Freezer(app.app)

@freezer.register_generator
def episode():
    for ep in app.get_eps():
        yield {'num': ep}

freezer.freeze()
