from django.contrib import admin
from . import models

class QuestiongroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'pub_date', 'owner', 'is_ongoing')

class QuestionAdmin(admin.ModelAdmin):
    list_display= ('question_text', 'pub_date', 'was_published_recently', 'get_group')

class ChoiceAdmin(admin.ModelAdmin):
    list_display= ('choice_text', 'get_question')
    

admin.site.register(models.Questiongroup, QuestiongroupAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Choice, ChoiceAdmin)
admin.site.register(models.Vote)
admin.site.register(models.Users_voted)