# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.contrib import admin
from adzone.models import Advertiser, AdCategory, AdZone, TextAd, BannerAd, FlashAd

class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']

class AdZoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description']

class TextAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url', 'content']

class BannerAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url']

class FlashAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'updated', 'enabled']
    list_filter = ['updated', 'enabled']
    search_fields = ['title', 'url']

admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(AdCategory)
admin.site.register(AdZone, AdZoneAdmin)
admin.site.register(TextAd, TextAdAdmin)
admin.site.register(BannerAd, BannerAdAdmin)
admin.site.register(FlashAd, FlashAdAdmin)
