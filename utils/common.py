from django.http import JsonResponse
import random,string

STATUS_CODE_MSG_MAP = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',

        400: 'Bad Request: The request cannot be fulfilled due to bad syntax',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Conflict',
        418: 'I\'m a teapot',      # RFC 2324 "Hyper Text Coffee Pot Control Protocol"
        423: 'Locked',
        422: 'Unprocessable Entities',
        429: 'Too many requests',

        501: 'Not implemented',
        500: 'Internal Server Error: Something is broken, try again later',
        503: 'Service Unavailable',
    }


#this program gives a proper output format
def response(code, custom_message=None):
    code_msg_map = STATUS_CODE_MSG_MAP
    try:
        code_msg = code_msg_map[code]
    except KeyError:
        code_msg = 'No message'
    response = {'status': {'code': code, 'message': custom_message or code_msg}, "data": None}
    return response

def get_order_no():
    # db=MongoDB().mongo.ammus
    # subscriptions = db.subscriptions
    # existing_subscriptions = subscriptions.find_one({'google_id' : google_id })
    x = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return x

def get_rand():
    # db=MongoDB().mongo.ammus
    # subscriptions = db.subscriptions
    # existing_subscriptions = subscriptions.find_one({'google_id' : google_id })
    x = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
    return x


