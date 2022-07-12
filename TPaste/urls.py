from django.urls import path
from django.views.generic import TemplateView

from Paste.views import (
    DetailPasteView,
    DetailPasteRawView,
    IndexView,
    DownloadPasteView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="paste_new"),
    path("<slug:paste_id>", DetailPasteView.as_view(), name="paste_details"),
    path("<slug:paste_id>/download", DownloadPasteView.as_view(), name="paste_download"),
    path("<slug:paste_id>/raw", DetailPasteRawView.as_view(), name="paste_details_raw"),

    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
