from .forms import LoginForm, CustomUserCreationForm

def auth_forms_context(request):
    """
    Adds login and signup forms to the context if the user is not authenticated.
    """
    context = {}
    if not request.user.is_authenticated:
        # Avoid adding forms if the user is already on the login/signup processing URL
        # to prevent potential infinite loops or unexpected behavior on error.
        # Note: This check might need adjustment depending on final URL structure.
        if request.path not in [request.build_absolute_uri(url) for url in ['/login/', '/signup/']]: # Basic check
             context['login_form'] = LoginForm(request=request) # Pass request for AuthenticationForm
             context['signup_form'] = CustomUserCreationForm()
    return context
