from polls.models import *
from django.contrib.auth.models import User
import datetime
import random
import time
from faker import Faker
fake = Faker()


def seed_users(num_entries=10, overwrite=False):
    """
    Creates num_entries worth a new users
    """
    if overwrite:
        print("Overwriting Users")
        users = User.objects.filter(is_superuser=False)
        users.delete()
    count = 0
    for _ in range(num_entries):
        first_name = fake.first_name()
        last_name = fake.last_name()
        u = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=first_name + "." + last_name + "@fakermail.com",
            username=first_name + last_name,
            password="password"
        )
        count += 1
        percent_complete = count / num_entries * 100
        print(
            "Adding {} new Users: {:.2f}%".format(
                num_entries, percent_complete),
            end='\r',
            flush=True
        )
    print()


def seed_groups(num_entries=6, q_min=3, q_max=4, choice_min=3, choice_max=4, overwrite=False):
    """
    Seeds num_entries poll with random users as owners
    Each poll will be seeded with # choices from choice_min to choice_max
    """
    if overwrite:
        print('Overwriting Polls, questions and choices')
        Questiongroup.objects.all().delete()
        Question.objects.all().delete()
        Choice.objects.all().delete()
    users = list(User.objects.all())
    count = 0
    for _ in range(num_entries):
        owner = random.choice(users)
        g = Questiongroup(
            owner=owner,
            group_name=f"{owner.username}_{owner.questiongroup_set.all().count()}",
        )
        g.save()

        count_q = 0

        num_questions = random.randrange(q_min, q_max + 1)
        for _ in range(num_questions):
            q = Question(
                group=g,
                question_text=f"{fake.sentence()} ?"
            )
            q.save()

            num_choices = random.randrange(choice_min, choice_max + 1)
            for _ in range(num_choices):
                c = Choice(
                    question=q,
                    choice_text=fake.sentence()
                )
                c.save()

            count_q += 1
            percent_complete = count_q / num_entries * 100
            print(
                "Adding {} new questions to {}: {:.2f}%".format(
                    num_entries, g.group_name, percent_complete),
                end='\r',
                flush=True
            )

        count += 1
        percent_complete = count / num_entries * 100
        print(
            "Adding {} new group : {:.2f}%".format(
                num_entries, percent_complete),
            end='\r',
            flush=True
        )
    print()


def seed_votes():
    """
    Creates a new vote on every poll for every user
    Voted for choice is selected random.
    Deletes all votes prior to adding new ones
    """
    Vote.objects.all().delete()
    Users_voted.objects.all().delete()

    users = User.objects.all()
    groups = Questiongroup.objects.all()

    count = 0
    total_user_count = users.count()
    for user in users:
        count += 1
        for g in groups:
            g.total_count += 1
            g.save()
            user_voted = Users_voted(
                user=user,
                group=g,
            )
            user_voted.save()

            questions = g.question_set.all()


            for q in questions:
                choices = q.choice_set.all()
                n = choices.count()
                i = random.randint(0, n)
                if i != n:
                    vote = Vote(
                        poller=user,
                        choice=choices[i],
                        question=q,
                        group=g,
                    )
                    vote.save()
        percent_complete = count / total_user_count * 100
        print(
            "_________Added new votes for {}: {:.2f}%_________".format(
                user.username, percent_complete),
            end='\r',
            flush=True
        )
    print()



def seed_all(num_entries=10, overwrite=True):
    """
    Runs all seeder functions. Passes value of overwrite to all
    seeder function calls.
    """
    start_time = time.time()
    # run seeds
    seed_users(num_entries=num_entries, overwrite=overwrite)
    seed_groups(num_entries=num_entries, overwrite=overwrite)
    seed_votes()
    # get time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print("Script Execution took: {} minutes {} seconds".format(minutes, seconds))
