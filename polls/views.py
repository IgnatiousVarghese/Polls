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
        'groups': groups,
        'back': "home",
    }
    return render(request, 'polls/group.html', context)


@login_required()
def edit(request):
    user = request.user
    groups = user.questiongroup_set.all()

    context = {
        'groups': groups,
        'back': "polls:group",
    }
    return render(request, 'polls/update/edit.html', context)


@login_required()
def add_group(request):
    user = request.user
    form = Groupform()

    if request.method == 'POST':
        form = Groupform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['group_name']
            if Questiongroup.objects.filter(group_name=name).count():
                form.add_error('group_name', "already taken")
            else:
                group = Questiongroup(owner=user, group_name=name)
                group.save()
                return redirect('polls:edit')

    context = {
        'form': form
    }

    return render(request, 'polls/add/form_group.html', context)


@login_required()
def group_delete(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    user = request.user

    group.delete()

    return redirect('polls:edit')


@login_required()
def group_rename(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    data = {
        'group_name': group.group_name
    }
    form = Groupform(initial=data)

    if request.method == 'POST':
        form = Groupform(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['group_name']
            if group.group_name == new_name:
                form.add_error('group_name', "not modified")
            elif Questiongroup.objects.filter(group_name=new_name).count():
                form.add_error('group_name', "already taken")
            else:
                group.group_name = new_name
                group.save()
                return redirect('polls:edit')

    context = {
        'form': form,
        'group': group
    }

    return render(request, 'polls/update/form_group.html', context)


@login_required()
def group_edit(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    questions = Question.objects.filter(group=group)
    ques_and_choices = {}
    for q in questions:
        ques_and_choices[q] = q.choice_set.all()

    context = {
        'group': group,
        'questions': questions,
        'ques_and_choices': ques_and_choices,
    }

    return render(request, 'polls/update/group_edit.html', context)


@login_required()
def add_question(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    data = {
        'group': group
    }
    form = Questionform(initial=data)

    if request.method == 'POST':
        form = Questionform(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            q = form.save()
            return redirect('polls:group_edit', group_name=group_name)

    context = {
        'form': form,
        'group_name': group_name
    }

    return render(request, 'polls/add/form_ques.html', context)


@login_required()
def question_change(request, group_name, q_id):
    group = Questiongroup.objects.get(group_name=group_name)
    q = Question.objects.get(id=q_id)
    data = {
        'question_text': q.question_text,
        'group': group
    }
    form = Questionform(initial=data)

    if request.method == 'POST':
        form = Questionform(request.POST)
        if form.is_valid():
            new_ques = form.cleaned_data['question_text']
            q.question_text = new_ques
            q.group = form.cleaned_data['group']
            q.save()
            return redirect('polls:group_edit', group_name=group_name)

    context = {
        'form': form,
        'group_name': group_name,
        'q_id': q_id,
    }

    return render(request, 'polls/update/form_ques.html', context)


@login_required()
def question_delete(request, group_name, q_id):
    group = Questiongroup.objects.get(group_name=group_name)
    q = Question.objects.get(id=q_id)

    q.delete()

    return redirect('polls:group_edit', group_name=group_name)


@login_required()
def add_choice(request, group_name, q_id):
    group = Questiongroup.objects.get(group_name=group_name)
    q = Question.objects.get(id=q_id)

    data = {
        'question': q,
    }

    form = Choiceform(initial=data)

    if request.method == 'POST':
        form = Choiceform(request.POST)
        if form.is_valid():
            choice = form.save()
            return redirect('polls:group_edit', group_name=group_name)

    context = {
        'form': form,
        'group': group,
        'question': q
    }

    return render(request, 'polls/add/form_choice.html', context)


@login_required()
def choice_edit(request, group_name, q_id, choice_id):
    group = Questiongroup.objects.get(group_name=group_name)
    q = Question.objects.get(id=q_id)
    choice = Choice.objects.get(id=choice_id)

    data = {
        'choice_text': choice,
        'question': q,
    }
    form = Choiceform(initial=data)

    if request.method == 'POST':
        form = Choiceform(request.POST)
        if form.is_valid():
            choice.choice_text = form.cleaned_data['choice_text']
            choice.save()
            return redirect('polls:group_edit',  group_name=group_name)

    context = {
        'form': form,
        'group': group,
        'question': q,
        'choice': choice,
    }

    return render(request, 'polls/update/form_choice.html', context)


@login_required()
def choice_delete(request, group_name, q_id, choice_id):
    group = Questiongroup.objects.get(group_name=group_name)
    q = Question.objects.get(id=q_id)
    choice = Choice.objects.get(id=choice_id)

    choice.delete()

    return redirect('polls:group_edit', group_name=group_name)


@login_required()
def index(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    user = request.user
    votes = Vote.objects.filter(poller=user).filter(group = group)
    questions = group.question_set.all()

    #
    voted_users = Users_voted.objects.filter(group=group).filter(user=user)
    if voted_users.count() == 0:
        group.total_count += 1
        user_voted = Users_voted(user=user, group=group)
        user_voted.save()
        group.save()
    #adding user to voted_user if he/she skipped index


    context = {
        'group': group,
        'votes': votes,
        'questions': questions
    }
    return render(request, 'polls/index.html', context)


@login_required()
def detail(request, group_name, question_no):
    user = request.user
    group = Questiongroup.objects.get(group_name=group_name)
    questions = group.question_set.all()

    ## can attemp questions only if group is OPEN
    if group.is_ongoing == False:
        return redirect('polls:group')

    ######

    voted_users = Users_voted.objects.filter(group=group).filter(user=user)
    if voted_users.count() == 0:
        return redirect('polls:index', group_name=group_name)
    #redirecting user to index if he/she skipped index

    if question_no <= 0:
        question_no = 1
    if question_no > len(questions):
        question_no = len(questions)

    question = questions[question_no-1]
    choices = question.choice_set.all()

    all_voted_q = []

    i = 0
    for q in questions:
        i += 1
        if user.vote_set.filter(question=q).exists():
            all_voted_q.append(i)

    is_voted = user.vote_set.filter(question=question)
    voted = None
    if is_voted.exists() > 0:
        voted = is_voted[0]

    last = False
    if question_no == len(questions):
        last = True

    context = {
        'group': group,
        'questions': questions,
        'question': question,
        'question_no': question_no,
        'last': last,
        'choices': choices,
        'voted': voted,
        'all_voted_q': all_voted_q,

    }
    return render(request, 'polls/detail.html', context)


@login_required()
def clear_choice(request, group_name, question_no, question_id):
    group = Questiongroup.objects.get(group_name=group_name)
    
    # can attemp questions only if group is OPEN
    if group.is_ongoing == False:
        return redirect('polls:group')

    user = request.user
    question = Question.objects.get(id=question_id)

    vote = user.vote_set.filter(question=question)
    if vote.exists():
        vote[0].delete()

    return redirect('polls:detail',
                    group_name=group_name,
                    question_no=question_no
                    )


@login_required
def vote(request, group_name, question_id):
    user = request.user
    group = Questiongroup.objects.get(group_name=group_name)
    
    # can attemp questions only if group is OPEN
    if group.is_ongoing == False:
        return redirect('polls:group')
        
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

    if request.method == 'POST' and group.is_ongoing:

        try:
            choice_id = request.POST['choice']
            choice = question.choice_set.get(id=choice_id)
            choice.save()

            vote = Vote()
            voted = user.vote_set.filter(question=question)
            if voted.count() > 0:
                vote = voted[0]
                vote.choice = choice
            else:
                vote = Vote(poller=user, group=group,
                            question=question, choice=choice)
            vote.save()

            return redirect('polls:detail', group_name=group.group_name, question_no=question_no+1)

        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            context = {
                'group': group,
                'question': question,
                'questions': questions,
                'choices': choices,
                'error_message': "you haven't chosen any options :)",
                'q_no': question_no
            }
            return render(request, 'polls/detail.html',  context)

    # return redirect('polls:result', question_id)

    return redirect('polls:group')


# open the poll only for creater
@login_required()
def startpoll(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    user = request.user
    if user == group.owner or user.is_superuser:
        group.is_ongoing = True
        group.save()
    return redirect('polls:group')


@login_required()
def endpoll(request, group_name):
    group = Questiongroup.objects.get(group_name=group_name)
    user = request.user
    if user == group.owner or user.is_superuser:
        group.is_ongoing = False
        group.save()
    return redirect('polls:group')


@login_required()
def result(request, group_name):
    user = request.user
    group = Questiongroup.objects.get(group_name=group_name)
    questions = group.question_set.all()
    votes = Vote.objects.filter(group=group)
    my_votes = Vote.objects.filter(group=group).filter(poller=user)

    total_votes = Users_voted.objects.filter(group=group).count()

    content = []
    for q in questions:
        choices = q.choice_set.all()
        q_result = {
            'question': q,
            'question_text': q.question_text,
            'labels': [],
            'count': [],
            'my_vote': 'None'
        }
        for c in choices:
            q_result['labels'].append(c.choice_text)
            count = votes.filter(choice=c).count()
            q_result['count'].append(count)

        if my_votes.filter(question=q).exists() > 0:
            q_result['my_vote'] = my_votes.filter(
                question=q)[0].choice.choice_text

        content.append(q_result)

    context = {
        'content': content,
        'group': group,
        'questions': questions,
        'my_votes': my_votes,
        'total_users_voted' : total_votes,
    }

    return render(request, 'polls/result.html', context)
