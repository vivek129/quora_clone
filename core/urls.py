from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('answer/<int:answer_id>/like/', views.like_answer, name='like_answer'),
    # Topic URLs
    path('topics/', views.topic_list, name='topic_list'),
    path('topic/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
    # Space URLs
    path('spaces/', views.space_list, name='space_list'),
    path('spaces/create/', views.create_space, name='create_space'),
    path('space/<slug:space_slug>/', views.space_detail, name='space_detail'),
    path('space/<slug:space_slug>/join/', views.join_leave_space, name='join_leave_space'),
    # Profile URL
    path('profile/', views.user_profile, name='user_profile'),
]
