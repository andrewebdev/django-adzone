# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django import template
from random import choice
import re
from django.contrib.contenttypes.models import ContentType
from adzone.models import AdImpression
from datetime import datetime

register = template.Library()

@register.tag(name='zone_ad')
def zone_ad(parser, token):
    """ This template tag returns a single ad from the database.
        ad_model is the advertising model
        The ad returned is random but must belong to the specified zone
    """
    try:
        tag_name, ad_model, arg = token.contents.split(None, 2)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name

    zone_slug, var_name = m.groups()

    if (ad_model[0] == ad_model[-1] and ad_model[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's arguments should not be in quotes" % tag_name

    if (zone_slug[0] == zone_slug[-1] and zone_slug[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's arguments should not be in quotes" % tag_name

    return ZoneAd(ad_model, zone_slug, var_name)

class ZoneAd(template.Node):
    """ This template tag returns a single ad from the database.
        ad_model is the advertising model ie textad or bannerad
        zone_slug is the slug for the specific zone to which the ad belongs

        Since we are viewing the ad (otherwise we would not show the url), we count this as a impression
    """
    def __init__(self, ad_model, zone_slug, var_name):
        self.ad_model, self.zone_slug = ad_model, zone_slug
        self.var_name = var_name

    def render(self, context):
        ad_type = ContentType.objects.get(app_label='adzone', model=self.ad_model)
        ad = choice(ad_type.model_class().objects.filter(zone__slug=self.zone_slug, enabled=True))
        if context.has_key('from_ip'):
            impression = AdImpression(content_object=ad, impression_date=datetime.now, source_ip=context['from_ip'])
            impression.save()
        context[self.var_name] = ad
        return ''
