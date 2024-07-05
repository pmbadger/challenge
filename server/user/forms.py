from django import forms
from .models import User
from .wallet import validate_wallet


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []

    def clean(self):
        cleaned_data = super().clean()

        wallet = cleaned_data.get("wallet")
        try:
            validate_wallet(wallet)
        except:
            raise forms.ValidationError({
                'wallet': "ETH wallets begin with 0x, and are followed by 40 alphanumeric characters"
                          " (numerals and letters), adding up to 42 characters in total"
            })
        return cleaned_data
