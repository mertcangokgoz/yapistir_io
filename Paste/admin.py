from django import forms
from django.contrib import admin

from .models import Paste, Report


class PasteAdminForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = '__all__'


class ReportAdminForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'


class PasteAdmin(admin.ModelAdmin):
    form = PasteAdminForm
    list_display = ['slug', 'publish', 'expire', 'view_count']
    readonly_fields = ['slug', 'publish', 'expire', 'view_count']
    search_fields = [
        'slug'
    ]


class ReportAdmin(admin.ModelAdmin):
    form = ReportAdminForm
    list_display = ['slugs_id', 'mail', 'reason', 'rapor_nedeni']
    readonly_fields = ['slugs_id', 'mail', 'reason', 'rapor_nedeni']
    search_fields = [
        'slugs_id'
    ]


admin.site.register(Paste, PasteAdmin)
admin.site.register(Report, ReportAdmin)
