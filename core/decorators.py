from django.shortcuts import redirect
from django.conf import settings
from functools import wraps

def login_required_modal(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url = request.get_full_path()  # current URL
            login_url = f"{settings.LOGIN_URL}?next={next_url}"
            if login_url == request.path:
                # Prevent redirect loop
                return redirect(settings.LOGIN_REDIRECT_URL)
            return redirect(login_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
