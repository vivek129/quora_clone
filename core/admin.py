from django.contrib import admin
from .models import Topic, Space, Question, Answer, Like

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'created_at')
    search_fields = ('name', 'description', 'owner__username')
    list_filter = ('created_at', 'owner')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('members',) # Easier to manage members

class AnswerInline(admin.TabularInline): # Or StackedInline for a different layout
    model = Answer
    extra = 1 # Number of empty forms to display
    fields = ('user', 'content', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'space', 'created_at')
    search_fields = ('title', 'content', 'user__username', 'space__name')
    list_filter = ('created_at', 'user', 'space', 'topics')
    filter_horizontal = ('topics',) # Easier to manage topics
    inlines = [AnswerInline] # Show answers directly on the question page

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'question', 'created_at')
    search_fields = ('content', 'user__username', 'question__title')
    list_filter = ('created_at', 'user')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'created_at')
    search_fields = ('user__username', 'answer__question__title')
    list_filter = ('created_at', 'user')
