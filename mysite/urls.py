
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.home, name = 'home'),
    path('check/' , views.check, name = 'check'),
    path('poll/', include('polls.urls'), name = 'polls'),
    path('accounts/', include('accounts.urls'), name = 'accounts'),
    path('tasks/' , include('tasks.urls'), name = 'tasks'),
]
