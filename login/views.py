from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib import messages

def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'registration_form.html', context)

def create_user(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'].lower(),
        password = hashedpw,
        birthday = request.POST['birthday']
    )
    return redirect('/wall_redirect')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['logemail'])
        request.session['user_id'] = user.id
        messages.success(request, "You have successfully logged in!")
        return redirect('/success')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'the_wall.html', context)

def logout(request):
    request.session.flush()
    
    return redirect('/')

def delete_user(request, id):
    x = User.objects.get(id = id)
    x.delete()
    return redirect('/')

def wall_index(request):
    return render(request, 'the_wall.html')