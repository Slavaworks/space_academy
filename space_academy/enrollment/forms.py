from django import forms

from .models import Candidates


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        exclude = ['mentor', 'is_padawan', 'answers']
