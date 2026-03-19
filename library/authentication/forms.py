from django import forms
from django.contrib.auth import authenticate

from .models import CustomUser


class CustomUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "middle_name", "last_name", "email", "role", "password"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        existing_user = CustomUser.get_by_email(email)
        if existing_user and existing_user.id != self.instance.id:
            raise forms.ValidationError("User with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        user.is_staff = user.role == 1

        if commit:
            user.save()

        return user


class LoginUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self._user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self._user = authenticate(
                self.request, email=email.strip(), password=password
            )
            if not self._user:
                raise forms.ValidationError("Invalid email or password.")

        return cleaned_data

    def get_user(self):
        return self._user
