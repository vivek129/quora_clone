from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import login_required_modal
from django.contrib import messages
from .models import Question, Answer, Like, Topic, Space
from .forms import CustomUserCreationForm, LoginForm, QuestionForm, AnswerForm, SpaceForm
from django.db.models import Count, Prefetch


def topic_list(request):
    topics = Topic.objects.annotate(num_questions=Count('questions')).order_by('-num_questions', 'name')
    return render(request, 'topic_list.html', {'topics': topics})


def topic_detail(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    questions = topic.questions.all().order_by('-created_at')
    question_form = QuestionForm()

    if request.method == 'POST' and request.user.is_authenticated:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.save()
            question.topics.set(question_form.cleaned_data['topics'])
            messages.success(request, f'Question posted in {topic.name}!')
            return redirect('core:topic_detail', topic_slug=topic.slug)

    return render(request, 'topic_detail.html', {
        'topic': topic,
        'questions': questions,
        'question_form': question_form
    })


def home(request):
    if request.method == 'POST' and request.user.is_authenticated:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.save()
            question.topics.set(question_form.cleaned_data['topics'])
            messages.success(request, 'Question posted successfully!')
            return redirect('core:home')
        questions = Question.objects.all().order_by('-created_at')
        return render(request, 'index.html', {'questions': questions, 'question_form': question_form})

    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'questions': questions,
        'question_form': QuestionForm()
    })


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
        else:
            error_message = "Registration failed. "
            for field, errors in form.errors.items():
                error_message += f"{field.capitalize()}: {', '.join(errors)} "
            messages.error(request, error_message.strip())
        referer = request.META.get('HTTP_REFERER', resolve_url('core:home'))
        return redirect(referer)
    return redirect('core:home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or resolve_url('core:home')
                if next_url in [
                    request.build_absolute_uri(resolve_url('core:login')),
                    request.build_absolute_uri(resolve_url('core:signup'))
                ]:
                    next_url = resolve_url('core:home')
                return redirect(next_url)
            messages.error(request, 'Login failed: Invalid username or password.')
        else:
            messages.error(request, 'Login failed: Please check your input.')
        referer = request.META.get('HTTP_REFERER', resolve_url('core:home'))
        return redirect(referer)
    return redirect('core:home')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')


@login_required_modal
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers.annotate(num_likes=Count('likes')).order_by('-num_likes', '-created_at')
    answer_form = AnswerForm()

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            messages.success(request, 'Your answer has been posted.')
            return redirect('core:question_detail', question_id=question.id)
        messages.error(request, 'There was an error posting your answer.')

    user_likes = set()
    if request.user.is_authenticated:
        user_likes = set(Like.objects.filter(user=request.user, answer__question=question).values_list('answer_id', flat=True))

    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
        'user_likes': user_likes
    })


@login_required_modal
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)

    if not created:
        like.delete()
        messages.info(request, 'You unliked the answer.')
    else:
        messages.success(request, 'You liked the answer.')

    return redirect('core:question_detail', question_id=answer.question.id)


def space_list(request):
    spaces = Space.objects.annotate(
        num_members=Count('members'),
        num_questions=Count('questions')
    ).order_by('-num_members', 'name')
    return render(request, 'space_list.html', {'spaces': spaces})


@login_required_modal
def create_space(request):
    if request.method == 'POST':
        form = SpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            space.members.add(request.user)
            messages.success(request, f'Space "{space.name}" created!')
            return redirect('core:space_detail', space_slug=space.slug)
        messages.error(request, 'Error creating space.')
    else:
        form = SpaceForm()
    return render(request, 'create_space.html', {'form': form})


def space_detail(request, space_slug):
    space = get_object_or_404(Space.objects.prefetch_related('members'), slug=space_slug)
    questions = space.questions.all().order_by('-created_at')
    question_form = QuestionForm()
    is_member = request.user.is_authenticated and request.user in space.members.all()

    if request.method == 'POST' and is_member:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.space = space
            question.save()
            question.topics.set(question_form.cleaned_data['topics'])
            messages.success(request, f'Question posted in {space.name}!')
            return redirect('core:space_detail', space_slug=space.slug)
        messages.error(request, 'Error posting question.')

    return render(request, 'space_detail.html', {
        'space': space,
        'questions': questions,
        'question_form': question_form,
        'is_member': is_member
    })


@login_required_modal
def join_leave_space(request, space_slug):
    space = get_object_or_404(Space, slug=space_slug)
    user = request.user

    if user == space.owner:
        messages.warning(request, "Owners cannot leave their own space.")
        return redirect('core:space_detail', space_slug=space.slug)

    if user in space.members.all():
        space.members.remove(user)
        messages.info(request, f'You have left the space "{space.name}".')
    else:
        space.members.add(user)
        messages.success(request, f'You have joined the space "{space.name}".')

    return redirect('core:space_detail', space_slug=space.slug)


@login_required
def user_profile(request):
    user_questions = Question.objects.filter(user=request.user).prefetch_related(
        Prefetch('answers', queryset=Answer.objects.order_by('-created_at'))
    ).order_by('-created_at')

    return render(request, 'profile.html', {'user_questions': user_questions})

