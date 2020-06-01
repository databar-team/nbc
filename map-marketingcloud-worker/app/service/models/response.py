from flask_restplus import Model, fields


def build_response(message):
    response = {
        'message': message
    }

    model = Model('PostResponse', {
        'message': fields.Raw(description='Message for post')
    })

    return response, model
