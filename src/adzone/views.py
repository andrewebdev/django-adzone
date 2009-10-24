# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from models import AdClick

def adView(request, model, id):
    """ First check whether the request came from this website
        If yes, record the click in the database, then redirect to ad url
        If no, 404
    """
    try:
        ad_type = ContentType.objects.get(app_label='adzone', model=model)
        ad = ad_type.get_object_for_this_type(id=id)
        click = AdClick(content_object=ad, click_date=datetime.now, source_ip=request.META.get('REMOTE_ADDR'))
        click.save()
    except:
        # we should raise a 404? or Bad Request?
        return HttpResponseNotFound()
    else:
        return HttpResponseRedirect(ad.url)
