from django.contrib import admin
from .models import Question, Answer, Report_Question, Report_Answer

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Report_Question)
admin.site.register(Report_Answer)
