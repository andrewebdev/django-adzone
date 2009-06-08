# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.contrib import admin
from adzone.models import Advertiser, AdCategory, AdZone, Ad

admin.site.register(Advertiser)
admin.site.register(AdCategory)
admin.site.register(AdZone)
admin.site.register(Ad)
