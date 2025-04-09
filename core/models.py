from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Topic(models.Model):
    """Represents a subject category for questions."""
    name = models.CharField(max_length=100, unique=True, help_text="The name of the topic.")
    slug = models.SlugField(max_length=110, unique=True, blank=True, help_text="URL-friendly version of the name, auto-generated.")
    description = models.TextField(blank=True, null=True, help_text="A brief description of the topic.")

    def save(self, *args, **kwargs):
        """Automatically generates a slug from the name if one doesn't exist."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the Topic model."""
        return self.name

class Space(models.Model):
    """Represents a community or group focused on a specific interest."""
    name = models.CharField(max_length=100, unique=True, help_text="The name of the space.")
    slug = models.SlugField(max_length=110, unique=True, blank=True, help_text="URL-friendly version of the name, auto-generated.")
    description = models.TextField(blank=True, help_text="A description of the space and its purpose.")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_spaces', help_text="The user who created and owns the space.")
    members = models.ManyToManyField(User, related_name='joined_spaces', blank=True, help_text="Users who are members of this space.")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically generates a slug from the name if one doesn't exist."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the Space model."""
        return self.name

class Question(models.Model):
    """Represents a question asked by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', help_text="The user who asked the question.")
    title = models.CharField(max_length=200, help_text="The main text of the question.")
    content = models.TextField(blank=True, help_text="Optional additional details or context for the question.")
    topics = models.ManyToManyField(Topic, related_name='questions', blank=True, help_text="Topics associated with this question.")
    space = models.ForeignKey(
        Space,
        on_delete=models.SET_NULL, # Keep question even if space is deleted
        null=True,
        blank=True,
        related_name='questions',
        help_text="The space this question belongs to, if any."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Question model."""
        return self.title

class Answer(models.Model):
    """Represents an answer provided by a user to a question."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', help_text="The user who wrote the answer.")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', help_text="The question this answer addresses.")
    content = models.TextField(help_text="The content of the answer.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Answer model."""
        return f"Answer to '{self.question.title}' by {self.user.username}"

class Like(models.Model):
    """Represents a user's 'like' on a specific answer."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', help_text="The user who liked the answer.")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes', help_text="The answer that was liked.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can only like an answer once
        unique_together = ('user', 'answer')

    def __str__(self):
        """String representation of the Like model."""
        return f"Like on answer to '{self.answer.question.title}' by {self.user.username}"
