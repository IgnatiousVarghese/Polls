from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.group, name= 'group'),

    path('edit/', views.edit, name = 'edit'),
    path('<str:group_name>/group/rename', views.group_rename, name = 'group_rename'),
    path('<str:group_name>/edit/', views.group_edit, name = 'group_edit'),

    
    
    path('<str:group_name>/', views.index, name = 'index'),
    path('<str:group_name>/<int:question_id>/', views.detail, name = 'detail'),
    path('<str:group_name>/<int:question_id>/vote/', views.vote, name = 'vote'),
    path('<str:group_name>/result/', views.result, name = 'result'),
    path('<str:group_name>/clearpoll/', views.clearpoll, name = 'clear_poll'),
]