from flask_restplus import Namespace, Resource

from config import title, version
from service.api.v1.controller.product_data_controller import ProductDataController
"""
This file defines endpoints for the Sales Force Marketing Cloud namespace API
"""

marketing_cloud_ns = Namespace(
    'marketing-cloud',
    description='Version {version} of {title} API'.format(title=title, version=version)
)


@marketing_cloud_ns.route('/product-data', methods=['POST'])
class ProductData(Resource):
    """Endpoints tied to the product data workflow with Sales Force Marketing Cloud"""
    @staticmethod
    def post():
        """ Activate the process of loading Sales Force Marketing Cloud API data into the database """
        return ProductDataController().post()
