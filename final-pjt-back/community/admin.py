from django.contrib import admin
from .models import Comment, Question, Vote, Review

admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Vote)
admin.site.register(Review)

