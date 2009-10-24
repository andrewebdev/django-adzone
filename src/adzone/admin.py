# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.contrib import admin
from adzone.models import *

class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']
    list_display = ['company_name', 'website', 'user']

class AdCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'slug']

class AdZoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description']

class AdBaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'since', 'updated', 'enabled']
    list_filter = ['updated', 'enabled', 'since', 'updated']
    search_fields = ['title', 'url']

class TextAdAdmin(AdBaseAdmin):
    search_fields = ['title', 'url', 'content']

class AdClickAdmin(admin.ModelAdmin):
    search_fields = ['ad', 'source_ip']
    list_display = ['ad', 'click_date', 'source_ip']
    list_filter = ['click_date']
    date_hierarchy = 'click_date'

class AdImpressionAdmin(admin.ModelAdmin):
    search_fields = ['ad', 'source_ip']
    list_display = ['ad', 'impression_date', 'source_ip']
    list_filter = ['impression_date']
    date_hierarchy = 'impression_date'

admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(AdCategory, AdCategoryAdmin)
admin.site.register(AdZone, AdZoneAdmin)
admin.site.register(TextAd, TextAdAdmin)
admin.site.register(BannerAd, AdBaseAdmin)
admin.site.register(AdClick, AdClickAdmin)
admin.site.register(AdImpression, AdImpressionAdmin)
