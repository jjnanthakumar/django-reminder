from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from .models import TodoList, Category, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
import logging


@login_required
def index(request):  # the index view
    # quering all todos with the object manager
    todos = TodoList.objects.filter(user=request.user)
    categories = Category.objects.all()  # getting all categories with object manager
    if request.method == "POST":  # checking if the request method is a POST
        if "taskAdd" in request.POST:  # checking if there is a request to add a todo
            title = request.POST["description"]  # title
            date = str(request.POST["date"])  # date
            category = request.POST["category_select"]  # category
            content = title + " -- " + date + " " + category  # content
            Todo = TodoList(user=request.user, title=title, content=content,
                            due_date=date, category=Category.objects.get(name=category))
            Todo.save()  # saving the todo
            return redirect("/")  # reloading the page
        if "taskDelete" in request.POST:  # checking if there is a request to delete a todo
            # checked todos to be deleted
            checkedlist = request.POST["checkedbox"]
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id))  # getting todo id
                todo.delete()  # deleting todo
        if "taskEdit" in request.POST:
            title = request.POST["description"]  # title
            date = str(request.POST["date"])  # date
            category = request.POST["category_select"]  # category
            content = title + " -- " + date + " " + category  # content
            Todo = TodoList(user=request.user, title=title, content=content,
                            due_date=date, category=Category.objects.get(name=category))
            Todo.save()  # saving the todo
            return redirect("/")  # r
    elif request.GET.get('id') is not None:
        id_ = request.GET.get('id')
        todo = TodoList.objects.get(id=id_)
        return render(request, "index.html", {"todos": todos, "edit_data": todo, "categories": categories})

    return render(request, "index.html", {"todos": todos, "categories": categories})


# Create a logger object to log necessary information
logger = logging.getLogger(__name__)

# User Login View


def register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email is already taken by others')
                return redirect('register')
            elif User.objects.filter(username=uname):
                messages.error(request, 'Username is taken by others')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=uname, email=email, password=password1)
                messages.success(request, 'Registration Success!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords does not match :(')
            return redirect('register')
    elif request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'Auth/register.html', {'title': 'Register'})


def login_user(request):
    if request.method == 'POST':
        # Use build-in authenticate function to authenticate user
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.get_username()}')
            return redirect('home')
        else:
            logger.info("Someone tried to login with invalid credentials")
            messages.warning(request, 'Invalid Credentials')
            return redirect('home')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'Auth/login.html', {'title': 'Login'})


@login_required
def logout_user(request):
    logger.info(f"User {request.user} Logged out Successfully!")
    messages.success(request, "Successfully Logged out :)")
    logout(request)
    return redirect('login')
