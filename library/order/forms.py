from django import forms
from order.models import Order
from book.models import Book
import datetime


class CreateOrderForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(count__gt=0),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='-- Select a book --',
        error_messages={'required': 'Please select a book.'}
    )
    plated_end_at = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=lambda: (datetime.date.today() + datetime.timedelta(days=14)),
        error_messages={'required': 'Please select a return date.'}
    )

    def clean_plated_end_at(self):
        date = self.cleaned_data.get('plated_end_at')
        if date and date <= datetime.date.today():
            raise forms.ValidationError('Return date must be in the future.')
        return date

    def clean_book(self):
        book = self.cleaned_data.get('book')
        if book and book.count <= 0:
            raise forms.ValidationError('This book is not available.')
        return book


class EditOrderForm(forms.Form):
    plated_end_at = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={'required': 'Please select a return date.'}
    )

    def clean_plated_end_at(self):
        date = self.cleaned_data.get('plated_end_at')
        if date and date <= datetime.date.today():
            raise forms.ValidationError('Return date must be in the future.')
        return date