from flask import Blueprint, Flask
from flask_restplus import Api
from service.api.v1.marketing_cloud import marketing_cloud_ns

from config import description, title, version


def create_application():
    """Creates the Flask application based on the provided blueprints"""
    app = Flask(__name__)

    blueprint_v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

    api_v1 = Api(
        blueprint_v1,
        title=f'{title} API',
        version=version,
        description=description
    )

    api_v1.add_namespace(marketing_cloud_ns)

    app.register_blueprint(blueprint_v1)

    return app
