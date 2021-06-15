from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.models import User
from .forms import *


@login_required()
def group(request):
    user = request.user
    groups = Questiongroup.objects.all()

    context = {
        'groups': groups
    }
    return render(request, 'polls/group.html', context)

@login_required()
def edit(request):
    user = request.user
    groups = Questiongroup.objects.all()

    context = {
        'groups': groups
    }
    return render(request, 'polls/edit.html', context)


@login_required()
def group_rename(request, group_name):
    group = Questiongroup.objects.get(group_name = group_name)
    data={
        'group_name' : group.group_name
    }
    form = Groupform(initial = data)

    if request.method == 'POST':
        form = Groupform(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['group_name']
            if group.group_name == new_name:
                form.add_error('group_name', "not modified")
            elif Questiongroup.objects.filter(group_name = new_name).count() :
                form.add_error('group_name', "already taken")
            else :
                group.group_name = new_name
                group.save()
                return redirect('polls:edit')

    context = {
        'form' : form,
        'group' : group
    }

    return render(request, 'polls/form.html', context)

@login_required()
def group_edit(request, group_name):
    group = Questiongroup.objects.get(group_name = group_name)
    questions = Question.objects.filter(group = group)

    context = {
        'group' : group,
        'questions' : questions
    }

    return render(request, 'polls/group_edit.html', context)


@login_required()
def index(request, group_name):
    group = Questiongroup.objects.get(group_name = group_name)
    user = request.user
    votes = Vote.objects.filter(poller=user).filter(question__group = group)
    questions = group.question_set.all()

    context = {
        'group': group,
        'votes': votes,
        'questions': questions
    }
    return render(request, 'polls/index.html', context)


@login_required()
def detail(request, group_name, question_id):
    user = request.user
    group = Questiongroup.objects.get(group_name=group_name)
    questions = group.question_set.all()
    question = None
    question_no = 0
    i = 0
    for q in questions:
        i += 1
        if q.id == question_id:
            question = q
            question_no = i

    choices = question.choice_set.all()
    is_voted = user.vote_set.filter(question = question)
    voted = None
    if  is_voted.count() > 0 :
        voted = is_voted[0]

    context = {
        'group': group,
        'question': question,
        'questions': questions,
        'choices': choices,
        'voted' : voted,
        'q_no' : question_no
    }
    return render(request, 'polls/detail.html', context)


@login_required
def vote(request, group_name, question_id):
    user = request.user
    group = Questiongroup.objects.get(group_name=group_name)
    questions = group.question_set.all()
    question = None
    question_no = 0
    i = 0
    for q in questions:
        i += 1
        if q.id == question_id:
            question = q
            question_no = i

    choices = question.choice_set.all()
    

    if request.method == 'POST':

        try:
            choice_id = request.POST['choice']
            choice = question.choice_set.get(id=choice_id)
            choice.votes += 1
            choice.save()

            vote = Vote()
            voted = user.vote_set.filter(question=question)
            if voted.count() > 0:
                vote = voted[0]
                vote.choice = choice
            else:
                vote = Vote(poller=user, question=question, choice=choice)
            vote.save()

            return redirect('polls:index', group_name=group.group_name)

        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            context = {
                'group': group,
                'question': question,
                'questions': questions,
                'choices': choices,
                'error_message' : "you haven't chosen any options :)",
                'q_no' : question_no
            }
            return render(request, 'polls/detail.html',  context)

    # return redirect('polls:result', question_id)

    return redirect('polls:group')


@login_required()
def clearpoll(request, group_name):
    group = Questiongroup.objects.get(group_name = group_name)
    user = request.user
    votes = Vote.objects.filter(poller = user).filter(question__group = group)
    for vote in votes:
        vote.delete()
    return redirect('polls:index', group_name)

@login_required()
def result(request):

    Q = Question.objects.all()
    questions = Question.objects.all()
    content = {}
    for q in Q:
        choices = q.choice_set.all()
        for c in choices:
            count = c.vote_set.all().count()
            if q.question_text in content:
                content[q.question_text] += [{c.choice_text: count}]
            else:
                content[q.question_text] = [{c.choice_text: count}]

    context = {
        'questions': questions
    }

    return render(request, 'polls/result.html', context)


