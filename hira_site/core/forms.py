from django import forms

from .models import QuoteRequest


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ["name", "email", "phone", "message"]
        labels = {"name": "Your name", "email": "Email", "phone": "Phone (optional)", "message": "What do you want to build?"}
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
