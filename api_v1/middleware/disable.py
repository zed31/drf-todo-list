
class DisableCSRF(object):
    """
        Django middleware used to disable the CSRF token
    """

    def __init__(self, get_response):
        """
            Initialize the DisableCSRF object

            :param get_response: Represent whatever comes next on the middleware chain
        """
        self.get_response = get_response

    def __call__(self, request):
        """
            Function used to call the middleware, it also calls the get_response
            which is the next middleware / view

            :param request: The request being processed
            :return: The response of the request
        """
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response
