from django import forms

class SizeForm(forms.Form):
    size = forms.CharField(label="validationCustom01", max_length = 2)


PAYMENT_CHOICES = (
    ('S', 'Card'),
    ('N', 'Numerar')
)


class CheckoutForm(forms.Form):
    nume = forms.CharField(required = True)
    prenume = forms.CharField(required=True)
    email = forms.CharField(required=True)
    adresa = forms.CharField(required=True)
    judet = forms.CharField(required = True)
    localitate =  forms.CharField(required = True)
    od_postal=forms.CharField(required=True)
    modalitate_de_plata = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
