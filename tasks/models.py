# tasks/models.py
from django.db import models
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('MISSING', 'Missing Deadline')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateTimeField()  # Changed from DateField to DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_overdue(self):
        """Check if the task is overdue and not completed"""
        return self.due_date < timezone.now() and self.status != 'DONE'
    
    def save(self, *args, **kwargs):
        # Check if deadline is missed and update status accordingly
        if self.due_date < timezone.now() and self.status not in ['DONE', 'MISSING']:
            self.status = 'MISSING'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']