import sys
import uuid

from django.contrib import messages
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from Paste.forms import (
    PasteForm,
)
from Paste.models import Paste


# Create your views here.
class IndexView(FormView):
    model = Paste
    form_class = PasteForm
    slug_url_kwarg = "paste_id"
    slug_field = "paste_id"
    template_name = "pages/index.html"

    def __init__(self, **kwargs):
        self.paste = None
        super().__init__(**kwargs)

    def form_valid(self, form):
        content_size = sys.getsizeof(form.cleaned_data["content"])
        if content_size <= 204800:  # 20M Limit
            self.paste = self.model.objects.create(
                content=form.cleaned_data["content"],
                title=form.cleaned_data["title"],
                lexer=form.cleaned_data["lexer"],
                expire=form.cleaned_data["expire"],
                size=content_size,
            )
            return super(IndexView, self).form_valid(form)
        else:
            messages.error(
                self.request, "Maximum 20MB boyutunda içerik girebilirsiniz."
            )
            return HttpResponseRedirect(reverse("paste_new"))

    def form_invalid(self, form):
        messages.error(self.request, "Kayıt sırasında bir sorun oluştu")
        return super(IndexView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "İçerik başarılı bir şekilde oluşturuldu")
        return reverse("paste_details", kwargs={"paste_id": self.paste.slug})


class DetailPasteView(DetailView):
    model = Paste
    slug_url_kwarg = "paste_id"
    slug_field = "slug"
    template_name = "pages/paste_details.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().is_removed:
            return HttpResponse(status=410)
        paste = self.get_object()
        paste.view_count += 1
        paste.save(update_fields=["view_count"])
        return super(DetailPasteView, self).get(request, *args, **kwargs)


class DetailPasteRawView(DetailView):
    model = Paste
    slug_url_kwarg = "paste_id"
    slug_field = "slug"
    template_name = "pages/paste_details_raw.html"

    def render_to_response(self, context, **kwargs):
        if self.get_object().is_removed:
            return HttpResponse(status=410)
        response = HttpResponse(self.get_object().content)
        response["Content-Type"] = "text/plain;charset=UTF-8"
        response["X-Content-Type-Options"] = "nosniff"
        return response


class DownloadPasteView(DetailView):
    model = Paste
    slug_url_kwarg = "paste_id"
    slug_field = "slug"
    template_name = "pages/paste_details_raw.html"

    def render_to_response(self, context, **kwargs):
        if self.get_object().is_removed:
            return HttpResponse(status=410)
        response = HttpResponse(self.get_object().content)
        response[
            "Content-Disposition"
        ] = f"attachment; filename={uuid.uuid4()}.txt"
        response["Content-Type"] = "text/plain; charset=UTF-8"
        response["X-Content-Type-Options"] = "nosniff"
        return response
