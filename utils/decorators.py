import jwt
from django.http import JsonResponse
import sys, os



def is_login(f):
    "this decorator checks the user login status"
    #@wraps(f)
    def decorated_function(*args, **kwargs):
        print("inside decorators")
        result = f(*args, **kwargs)  # Call Function
        return result
    return decorated_function




def validate(function):

    """Decorator to validate JWT token. file location-woohoonlu/decorators.py

    Args: function/view.
    
    Returns: Function(request,userId) if validation successful, Status 401 if not successful
    """

    def wrap(request, *args, **kwargs):
        key = "woohooenterprisesecret"
        try:
            auth = request.META['HTTP_AUTHORIZATION']
            decoded = jwt.decode(auth, key, algorithms=['HS256'], verify=False)
            request.uid = decoded["domainId"]

            try:

                return function(request)
            except TypeError:
                return function(request, *args)

        except KeyError as e:
            if str(e) == '\'HTTP_AUTHORIZATION\'':
                response = dict(success=False, message="No token provided", error=str(e))
                return JsonResponse(response, status=401)
            else:
                response = {'success': False, 'message': 'Key-error', 'error': str(e)}
                print(str(e))
                return JsonResponse(response, status=406)


    wrap._doc_ = function._doc_
    wrap._name_ = function._name_
    return wrap