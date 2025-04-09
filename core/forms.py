from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Question, Answer, Topic, Space # Import Space model
from django.forms import TextInput, Textarea, EmailInput, PasswordInput, CheckboxSelectMultiple # Import specific widgets

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mb-2'}) # Add class to all fields

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email (Optional)'}),
        }


class LoginForm(AuthenticationForm):
     username = forms.CharField(widget=TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Username'}))
     password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Password'}))

class QuestionForm(forms.ModelForm):
    # Make topics optional and use checkboxes
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all().order_by('name'),
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'topics'] # Add topics field
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Start your question with "What", "How", "Why", etc.'}),
            'content': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional: Add more details...'}),
    
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your answer here...', 'rows': 4}),
        }
        labels = {
            'content': '' # Hide the default label for a cleaner look
        }

class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of your space'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your space (optional)'}),
        }
