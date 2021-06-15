import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Questiongroup(models.Model):
    group_name = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('published date', auto_now_add= True)
    
    def __str__(self):
        return self.group_name


class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('published date', auto_now_add= True)
    group = models.ForeignKey(Questiongroup, on_delete= models.CASCADE)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now + datetime.timedelta(days=1) >= self.pub_date >= now - datetime.timedelta(days=1)

    def can_vote(self, user):
        votes = user.vote_set.filter(question = self)
        if votes.exists():
            return True
        return False
    
    def count_votes(self):
        return self.vote_set.count()
    
    def get_group(self):
        return self.group
        


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def get_question(self):
        return self.question

class Vote(models.Model):
    poller = models.ForeignKey(User, on_delete= models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.poller.username) + ":" + str(self.question)[:8]+":"+ str(self.choice)[:8]
