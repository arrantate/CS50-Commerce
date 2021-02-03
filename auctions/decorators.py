from django.shortcuts import redirect

def user_is_authenticated(function):

    def wrapper(request, *args, **kwargs):
        user=  request.user  
        if user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper