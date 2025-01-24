from django import forms
from .models import Task

class ItemForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['TaskName', 'Date', 'Priority']