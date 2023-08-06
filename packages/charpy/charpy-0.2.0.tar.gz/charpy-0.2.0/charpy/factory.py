# -*- coding: utf-8 -*-
"""
Use export FLASK_APP="charpy.factory:create_app()"


"""
from flask import Flask

from charpy.blueprints.simple_page import simple_page


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    # add your modules
    app.register_blueprint(simple_page)

    return app


if __name__ == "__main__":
    app = create_app( debug=True)
    app.run()