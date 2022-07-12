import string
from datetime import datetime
from random import SystemRandom
from typing import final

from django.contrib.postgres.indexes import BTreeIndex
from django.db import models
from django.utils import timezone
from safedelete.models import SafeDeleteModel

from Paste.highlight import pygmentize


@final
class Paste(SafeDeleteModel):
    content = models.TextField()
    highlighted = models.TextField(blank=True, editable=False)
    size = models.IntegerField()
    title = models.CharField(max_length=160, blank=True)
    publish = models.DateTimeField(auto_now_add=True)
    lexer = models.CharField(max_length=60, editable=False)
    expire = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    view_count = models.PositiveIntegerField(default=0)
    is_dmca = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-publish"]
        managed = True
        verbose_name = "Paste"
        verbose_name_plural = "Pastes"
        indexes = [
            BTreeIndex(fields=["slug"], name="slug_idx"),
        ]

    def __str__(self):
        return f"{self.title} - {self.lexer} - {self.size} bytes"

    def highlight(self):
        return pygmentize(self.content, self.lexer)

    @staticmethod
    def generate_secret_id(length=3, max_loop=32) -> str:
        loop = 0
        while True:
            slug = "".join(
                [
                    SystemRandom().choice(string.ascii_letters + string.digits)
                    for _ in range(length)
                ]
            )
            try:
                Paste.objects.get(slug=slug)
            except Paste.DoesNotExist:
                return slug
            if loop >= max_loop:
                length += 1
            loop += 1

    @staticmethod
    def get_expire(date: datetime) -> str:
        if date == "never":
            converted_date = None
        if date == "90d":
            converted_date = timezone.now() + timezone.timedelta(days=90)
        if date == "30d":
            converted_date = timezone.now() + timezone.timedelta(days=30)
        if date == "7d":
            converted_date = timezone.now() + timezone.timedelta(days=7)
        return converted_date  # noqa

    @staticmethod
    def get_line_count(content):
        return len(content.splitlines())

    def save(self, *args, **kwargs):
        if self.view_count:
            pass
        else:
            self.expire = self.expire
            self.title = self.title
            self.expire = self.get_expire(self.expire)
            self.slug = self.generate_secret_id()
            self.content = self.content
            self.highlighted = self.highlight()
        super(Paste, self).save(*args, **kwargs)
