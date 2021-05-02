from django import forms

from .models import Order


class DateInput(forms.DateInput):
    input_type = 'date'

class OrderForm(forms.ModelForm):

    # order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))


    class Meta:
        model = Order
        widgets = {
            'order_date': DateInput()
        }
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'order_date',
            'comment'
        )