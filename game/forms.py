from django import forms
from .models import Game, GameCategory


class uploadGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['']
