from django import forms

from .models import Author


class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "surname", "patronymic"]

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        return name

    def clean_surname(self):
        surname = (self.cleaned_data.get("surname") or "").strip()
        if not surname:
            raise forms.ValidationError("Surname is required.")
        return surname

    def clean_patronymic(self):
        patronymic = (self.cleaned_data.get("patronymic") or "").strip()
        if not patronymic:
            raise forms.ValidationError("Patronymic is required.")
        return patronymic
