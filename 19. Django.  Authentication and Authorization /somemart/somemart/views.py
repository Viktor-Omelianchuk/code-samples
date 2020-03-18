def basicauth(view_func):
    """Decorator implementing HTTP Basic AUTH."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    token = base64.b64decode(auth[1].encode('ascii'))
                    username, password = token.decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        request.user = user
                        return view_func(request, *args, **kwargs)

        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="Somemart staff API"'
        return response
    return _wrapped_view


def staff_required(view_func):
    """Decorator checking the presence of the is_staff flag for the user."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        response = HttpResponse(status=403)
        return response
    return _wrapped_view


from django.utils.decorators import method_decorator


@method_decorator(basicauth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class AddItemView(View):
    pass
    