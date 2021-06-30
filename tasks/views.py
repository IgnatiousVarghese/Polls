from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import TaskForm, updateForm
from .models import Task

# Create your views here.


def index(request):
    user = request.user
    tasks = Task.objects.none()
    if user.is_authenticated:
        tasks = Task.objects.filter(author__id=user.id)
    else:
        tasks = Task.objects.filter(author__id=None)
    form = TaskForm()

    if request.method == 'POST':
        if user.is_authenticated:
            form = TaskForm(request.POST)
            if form.is_valid():
                user_task = form.save()
                user_task.author = user
                user_task.save()
        else:
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()

        return redirect('tasks:tasks')

    content = {'tasks': tasks, 'form': form, 'user': user}
    return render(request, 'tasks/list.html', content)


def delete(request, id):
    task = Task.objects.get(id=id)
    if task:
        task.delete()
    return redirect('tasks:tasks')


def update(request, id):
    task = Task.objects.get(id=id)
    form = updateForm(instance=task)
    if request.method == 'POST':
        form = updateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('tasks:tasks')

    content = {'task': task, 'form': form}
    return render(request, 'tasks/update_task.html', content)
