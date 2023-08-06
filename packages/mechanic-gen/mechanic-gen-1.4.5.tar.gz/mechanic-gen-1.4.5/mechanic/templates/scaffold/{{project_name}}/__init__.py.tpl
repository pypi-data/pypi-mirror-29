# mechanic save - safe to modify below #
from flask import Flask


def create_app():
    app = Flask('{{project_name}}')
    # If you are using SQLAlchemy, you can initialize your db here
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'your db uri'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # from {{ project_name }}.models import db
    # db.init_app(app)
    from {{project_name}}.blueprints import {{project_name}}_blueprint
    app.register_blueprint({{project_name}}_blueprint)

    # To disable documentation, remove blueprint below
    from mechanic.openapi import openapi_blueprint
    app.register_blueprint(openapi_blueprint)

    import logging
    logger = logging.getLogger('{{project_name}}')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return app
# END mechanic save #
