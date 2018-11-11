
def is_user_authenticated(request):
    """
        Check if the session exist inside the specified
        request

        :param request: The request being analyzed
    """
    return request.session.session_key

def is_user_admin(request):
    """
        Check if the user is an administrator

        :param request: The request sent by the user
    """
    return request.user.is_superuser
