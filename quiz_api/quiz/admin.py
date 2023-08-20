from django.contrib import admin

from .models import Quiz, Question, Answer, ResultAnswer


class QuizAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ResultAnswer)
