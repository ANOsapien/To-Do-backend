from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control priority-dropdown'})
    )

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']