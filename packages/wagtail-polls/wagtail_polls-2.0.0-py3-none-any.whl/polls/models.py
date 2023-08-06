from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.html import strip_tags
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import Orderable
from wagtail.core.fields import RichTextField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey


@register_snippet
class Poll(ClusterableModel, models.Model):
    name = models.CharField(max_length=200)
    message = RichTextField(
        blank=True,
        help_text=_("Copy to show on the poll. For example a question."))

    panels = [
        FieldPanel('name'),
        FieldPanel('message'),
        InlinePanel('pollitem_set', label=_("Choices")),
    ]

    def __str__(self):
        return self.name


class PollItem(Orderable, models.Model):
    poll = ParentalKey(Poll, related_name="pollitem_set")
    message = RichTextField(
        blank=True,
        verbose_name=_("Choice"),
    )

    panels = [
        FieldPanel('message'),
    ]

    def __str__(self):
        return strip_tags(self.message)


class Vote(models.Model):
    item = models.ForeignKey(PollItem)
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return '{} {}'.format(self.user, self.item)

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        qs = Vote.objects.filter(user=self.user, item__poll=self.item.poll)
        if qs.exists():
            raise ValidationError({'item': ['Item and user must be unique']})
