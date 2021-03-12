from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated(func):
    def wrapper(r,*args,**kwargs):
        if r.user.is_authenticated:
            return redirect("home")
        else:
            return func(r,*args,**kwargs)
    return wrapper


def allow(allowed_roles=[]):
    def decorator(func):
        def wrapper(r,*args,**kwargs):
            group=None
            if r.user.groups.exists():
                group=r.user.groups.all()[0].name
            print(group)
            if group in allowed_roles:
                return func(r,*args,**kwargs)
            else:
                return HttpResponse("your not authorized to view this page")
        return wrapper
    return decorator

def adminonly(func):
    def wrapper(r,*args,**kwargs):
        group=None
        if r.user.groups.exists():
            group=r.user.groups.all()[0].name
        if group=="admin":
            return func(r,*args,**kwargs)
        else:
            return redirect("user")
    return wrapper
