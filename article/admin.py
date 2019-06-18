from django.contrib import admin
from .models import Article, Comment, Report_Article, Report_Commit

# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Report_Article)
admin.site.register(Report_Commit)
