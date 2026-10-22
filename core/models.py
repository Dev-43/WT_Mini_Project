from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Role(models.Model):
    """Job role representing industry career tracks (e.g. Full Stack Developer)."""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual technical or soft skill required across engineering roles."""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, default='General', help_text="e.g. Frontend, Backend, Database, Core CS")

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class RoleSkill(models.Model):
    """Mapping between a Role and required Skills with required proficiency (1 to 5)."""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='role_skills')
    required_level = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Proficiency level on a scale of 1 to 5"
    )

    class Meta:
        unique_together = ('role', 'skill')
        ordering = ['role', 'skill']

    def __str__(self):
        return f"{self.role.name} -> {self.skill.name} (Req: {self.required_level})"


class Profile(models.Model):
    """Extended user profile storing college, academic year, and target role."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    college = models.CharField(max_length=200, blank=True, default='AISSMS IOIT')
    year = models.CharField(
        max_length=50,
        blank=True,
        default='Third Year',
        choices=[
            ('First Year', 'First Year (FE)'),
            ('Second Year', 'Second Year (SE)'),
            ('Third Year', 'Third Year (TE)'),
            ('Final Year', 'Final Year (BE)'),
        ]
    )
    target_role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aspiring_students'
    )

    def __str__(self):
        return f"{self.user.username} - {self.college} ({self.year})"


class UserSkill(models.Model):
    """User's self-assessed proficiency for a skill (0 to 5)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    current_level = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Current proficiency level from 0 (none) to 5 (expert)"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['skill__name']

    def __str__(self):
        return f"{self.user.username}: {self.skill.name} = {self.current_level}"


class Resource(models.Model):
    """Curated learning resource for bridging skill gaps."""
    RESOURCE_TYPES = [
        ('Course', 'Course'),
        ('Video', 'Video'),
        ('Book', 'Book'),
        ('Article', 'Article'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    link = models.URLField(help_text="Valid HTTP or HTTPS link to resource")
    type = models.CharField(max_length=50, choices=RESOURCE_TYPES, default='Course')

    class Meta:
        ordering = ['skill', 'type', 'title']

    def __str__(self):
        return f"[{self.type}] {self.title} ({self.skill.name})"


class Progress(models.Model):
    """Learning tracker progress per skill and optional resource."""
    STATUS_CHOICES = [
        ('Not started', 'Not started'),
        ('In progress', 'In progress'),
        ('Done', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='progress_records')
    resource = models.ForeignKey(
        Resource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='progress_records'
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Not started')
    notes = models.TextField(blank=True, help_text="Key takeaways, projects built, or notes")
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} [{self.status}]"
