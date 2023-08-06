from django import template
from polls.models import Vote
register = template.Library()


@register.assignment_tag()
def check_if_voted(poll, user):
    if user.is_authenticated() is False:
        return False
    return Vote.objects.filter(
        item__poll=poll,
        user=user,
    ).exists()
