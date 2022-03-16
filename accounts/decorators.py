
from django.http import HttpResponse
from django.shortcuts import redirect

"""decorators allow users to direct not logged users to login page and
logged users to dashboard"""
def unauthenticated_user(view_fun):
    def wrraper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fun(request,  *args, **kwargs)
    return wrraper_fun


def allowed_users(allowed_roles = []):
    def decorator(view_fun):
        def wrapper_fun(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles: 
                return view_fun(request, *args, **kwargs)
            else:
                return HttpResponse('Sorry! You are not authorized to login.')
        return wrapper_fun
    return decorator
    

# adding admin only pages
def admin_only(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'Customer':
            return redirect('user')

        if group == 'Admin':
            return view_fun(request, *args, **kwargs)
    return wrapper_fun

    