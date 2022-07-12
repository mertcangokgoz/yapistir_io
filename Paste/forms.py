import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.widgets import Textarea, Select

from Paste.highlight import LEXER_CHOICES

EXPIRE_CHOICES = (
    ("7d", "Yedi gün sonra yok et"),
    ("30d", "Bir ay sonra yok et"),
    ("90d", "Doksan gün sonra yok et"),
    ("never", "Asla yok etme"),
)

EXPIRE_DEFAULT = "never"

"""
    yapıştırma içerik form alanı
"""


class PasteForm(forms.Form):
    lexer = forms.ChoiceField(
        choices=LEXER_CHOICES,
        widget=Select(attrs={"class": "input select2"}),
    )

    expire = forms.ChoiceField(
        choices=EXPIRE_CHOICES,
        initial=EXPIRE_DEFAULT,
        widget=Select(attrs={"class": "input", "id": "id_expire"}),
    )

    title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "input", "autocomplete": "off", "placeholder": "Konu", }
        ),
    )

    content = forms.CharField(
        required=True,
        widget=Textarea(
            attrs={"class": "textarea", "rows": "10", "placeholder": "İçerik..."}
        ),
    )

    g_recaptcha_response = forms.CharField()

    def clean(self):
        data = self.cleaned_data.get("g_recaptcha_response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": data,
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        status = verify_rs.get("success", False)
        score = verify_rs.get("score", 0)
        if not status and score < 0.5:
            raise forms.ValidationError(
                "Bot doğrulama başarısız, Lütfen VPN veya Proxy kapatın.",
                code="invalid",
            )

    def clean_title(self):
        data = self.cleaned_data.get("title")
        if len(data) > 160:
            raise ValidationError("Maximum 160 karakter girebilirsiniz.")
        return data

    def clean_content(self):
        data = self.cleaned_data.get("content")
        if not data:
            raise ValidationError("İçerik girişi yapmalısınız.")
        return data
