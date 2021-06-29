from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.group, name= 'group'),
    path('startpoll/<str:group_name>/', views.startpoll, name = 'startpoll'),
    #for start the paused  poll --only for owner of group
    path('endpoll/<str:group_name>/', views.endpoll, name = 'endpoll'),
    #for finishing the poll --only for owner of group

    path('edit/', views.edit, name = 'edit'),

    path('edit/<str:group_name>/group_edit', views.group_edit, name = 'group_edit'),
    path('edit/<str:group_name>/group_rename', views.group_rename, name = 'group_rename'),
    path('edit/<str:group_name>/group_delete', views.group_delete, name = 'group_delete'),
    #for editing questions in group
    
    path('edit/<str:group_name>/question_change/<int:q_id>/', views.question_change, name = 'question_change'),
    path('edit/<str:group_name>/question_delete/<int:q_id>/', views.question_delete, name = 'question_delete'),
    #for editing choices in question

    path('edit/<str:group_name>/choice_edit/<int:q_id>/<int:choice_id>/', views.choice_edit, name = 'choice_edit'),
    path('edit/<str:group_name>/choice_delete/<int:q_id>/<int:choice_id>/', views.choice_delete, name = 'choice_delete'),
    #for editing a choice in question

    path('edit/add_group/', views.add_group, name = 'add_group'),
    path('edit/add_question/<str:group_name>/', views.add_question, name = 'add_question'),
    path('edit/add_choice/<str:group_name>/<int:q_id>/', views.add_choice, name = 'add_choice'),
    
    
    path('<str:group_name>/', views.index, name = 'index'),
    path('<str:group_name>/<int:question_no>/', views.detail, name = 'detail'),

    path('<str:group_name>/<int:question_no>/clear_choice/<int:question_id>/', views.clear_choice, name = 'clear_choice'),
    #clear selected choice for a question
    
    path('<str:group_name>/<int:question_id>/vote/', views.vote, name = 'vote'),

    path('<str:group_name>/result/', views.result, name = 'result'),


]