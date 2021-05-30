from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import get_object_or_404
from .models import Question, Choice, Vote
from django.contrib.auth.models import User


@login_required()
def index(request):
    user = request.user
    votes = Vote.objects.filter(poller=user)
    questions = Question.objects.all()

    context = {
        'votes': votes,
        'questions': questions
    }
    return render(request, 'polls/index.html', context)


@login_required()
def detail(request, question_id):
    questions = Question.objects.all()
    question = get_object_or_404(Question, id=question_id)
    choices = question.choice_set.all()

    content = {
        'question': question,
        'questions': questions,
        'choices': choices
    }
    return render(request, 'polls/detail.html', content)


@login_required
def vote(request, question_id):
    question = Question.objects.get(id=question_id)
    choices = question.choice_set.all()
    user = request.user

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

            return redirect('polls:index')

        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'choices': choices,
                'error_message': "You didn't select a choice.",
            })

    return redirect('polls:result', question_id)

    content = "You're voting on question . " + str(question_id) + "<br><br>"
    content += "your choice is : " + choice.choice_text
    return HttpResponse(content)


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
        'questions' : questions
    }

    return render(request, 'polls/result.html', context)

@login_required()
def clearpoll(request):
    user = request.user
    votes = user.vote_set.all()
    for vote in votes:
        vote.delete()
    return redirect('home')
