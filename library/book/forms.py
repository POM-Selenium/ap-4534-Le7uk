from django import forms
from book.models import Book
from author.models import Author


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Please select at least one author.'}
    )

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 128}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        error_messages = {
            'name': {'required': 'Book name is required.', 'max_length': 'Name must be at most 128 characters.'},
            'description': {'required': 'Description is required.', 'max_length': 'Description must be at most 256 characters.'},
        }

    def clean_count(self):
        count = self.cleaned_data.get('count')
        if count is None:
            raise forms.ValidationError('Count is required.')
        if count < 0:
            raise forms.ValidationError('Count cannot be negative.')
        return count

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError('Book name is required.')
        return name.strip()