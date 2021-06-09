from django.http import HttpResponse
from django.shortcuts import redirect


def product_manager(view_func):
    def wrapper_func(request, *args, **kwargs):
        group_list = []
        user = request.user
        for groups in user.groups.all():
            group_list.append(groups.name)
        if 'product manager' in group_list:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('store')
    return wrapper_func

def sales_manager(view_func):
    def wrapper_func(request, *args, **kwargs):
        group_list = []
        user = request.user
        for groups in user.groups.all():
            group_list.append(groups.name)
        if 'sales manager' in group_list:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('store')
    return wrapper_func