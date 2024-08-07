from typing import Any
from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class BookForm(forms.ModelForm):
    author_existing = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)
    author_new = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Book
        fields = ['title', 'description', 'author_existing', 'author_new']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['author_existing'].queryset = Author.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        author_existing = cleaned_data.get('author_existing')
        author_new = cleaned_data.get('author_new')

        if not author_existing and not author_new:
            raise forms.ValidationError('Debes seleccionar un autor existente o agregar uno nuevo.')

        if author_existing and author_new:
            raise forms.ValidationError('Solo puedes seleccionar un autor existente o agregar uno nuevo, no ambos.')

        return cleaned_data


