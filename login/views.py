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
        new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'].lower(),
        password = hashedpw,
        birthday = request.POST['birthday']
    )
    request.session['user_id'] = new_user.id
    return redirect('/wall')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['log_email'])
        request.session['user_id'] = user.id
        return redirect('/wall')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    messages = Message.objects.all()
    comments = Comment.objects.all()
    wall_test = [messages]
    context = {
        'user': user,
        'messages': messages,
        'comments': comments,
        'wall_test': wall_test
        
    }
    return render(request, 'the_wall.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def delete_user(request, id):
    x = User.objects.get(id = id)
    x.delete()
    return redirect('/')

def create_message(request):
    Message.objects.create(
        user = User.objects.get(id=request.session['user_id']),
        message = request.POST['user_message']
    )
    return redirect('/wall')

def create_comment(request, id):
    Comment.objects.create(
        user = User.objects.get(id=request.session['user_id']),
        message = Message.objects.get(id=id),
        comment = request.POST['user_comment']
    )
    return redirect('/wall')

def delete_message(request, id):
    x = Message.objects.get(id=id)
    x.delete()
    return redirect ('/wall')