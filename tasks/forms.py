from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Set initial values for datetime-local inputs
        if self.instance.pk and self.instance.due_date:
            # Format the datetime for the datetime-local input
            self.initial['due_date'] = self.instance.due_date.strftime('%Y-%m-%dT%H:%M')