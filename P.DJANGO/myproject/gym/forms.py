from django import forms
from .models import Membership

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['name', 'last_name', 'mobile_number', 'email', 'age', 'gender', 'membership_plan', 'tenure', 'payment_status', 'start_date', 'end_date']
