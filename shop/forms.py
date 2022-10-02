from django import forms

from shop.models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата доставки (самовывоза) заказа'


    order_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'delivery', 'order_date', 'comment'
        )
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }