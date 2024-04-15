from django.shortcuts import render, redirect

from loginapp import models


# this function will render to root route, Registration/Login page
def index(request):
    return render(request, 'index.html')


# this function for registration
def register(request):
    models.register(request)
    return redirect('/')


def log_in(request):
    models.log_in(request)
    return redirect('/success')


def success(request):
    if 'user_id' in request.session:
        context = {
            'user': models.User.objects.get(id=request.session['user_id'])
        }
        return render(request, "success.html", context)
    else:
        return redirect('/')


def log_out(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
