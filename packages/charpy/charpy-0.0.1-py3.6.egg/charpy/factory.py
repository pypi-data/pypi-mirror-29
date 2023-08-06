# -*- coding: utf-8 -*-
"""
Use export FLASK_APP="charpy.factory:create_app()"


"""
from flask import Flask
from werkzeug.utils import find_modules, import_string


def create_app(config=None):
    app = Flask('charpy')

    app.config.update(config or {})

    register_blueprints(app)
    register_cli(app)

    return app


def register_blueprints(app):
    """
    Register all blueprint modules

    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def register_cli(app):
    @app.cli.command('help')
    def help_command():
        """Calling for help"""
        print('You are calling for help')