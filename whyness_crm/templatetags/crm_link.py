#----------------------------------------------------------------------
# Whyness crm templatetags
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import logging

from django import template
from django.urls import reverse, NoReverseMatch
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

from whyness_crm.models import TrackerDestination

register = template.Library()

logger = logging.getLogger(__name__)

@register.simple_tag(takes_context=True)
def crm_link(context, link, title=None):
    """Adds a trackable link"""
    user = context['user']
    msg = 'CRMLink: {}'.format(context)
    logger.debug(msg)
    msg = 'CRMLink: {} : {}'.format(user, link)
    logger.debug(msg)

    try:
        link = TrackerDestination.objects.get(url=link)
    except TrackerDestination.DoesNotExist:
        link = TrackerDestination(url=link)
        link.save()

    site = Site.objects.get_current()
    ret_domain = site.domain
    try:
        ret_path = reverse('crm-tracker', args=[link.xref, str(user.xref)])
    except NoReverseMatch:
        ret_path = reverse('whyness_crm:tracker', args=[link.xref, str(user.xref)])
    ret_url = "https://{}{}".format(ret_domain, ret_path)
    if title:
        ret = '<a href="{}">{}</a>'.format(ret_url, title)
    else:
        ret = '<a href="{}">{}</a>'.format(ret_url, ret_url)
    logger.debug(ret)
    return mark_safe(ret)
