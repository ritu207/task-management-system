from django.db import models

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Employee Model
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self):
        return self.title

    # Custom validation
    def clean(self):
        if self.assigned_to:
            pending_tasks = Task.objects.filter(
                assigned_to=self.assigned_to,
                status='Pending'
            ).exclude(pk=self.pk).count()  # Exclude current instance when editing

            if pending_tasks >= 5:
                raise ValidationError(
                    f"{self.assigned_to.name} already has 5 pending tasks. "
                    "Cannot assign more than 5 pending tasks."
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called on save
        super().save(*args, **kwargs)

    # Calculated field: Days left
    @property
    def days_left(self):
        return (self.due_date - date.today()).days