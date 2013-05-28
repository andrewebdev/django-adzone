# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
try:
    from django.utils.timezone import now, make_aware, utc
except ImportError:
    now = datetime.datetime.now
    make_aware = None

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        AdBase = orm['adzone.adbase']
        if make_aware is None:
            max_dt = datetime.datetime.max
        else:
            max_dt = make_aware(datetime.datetime.max, utc)

        ads_enabled = AdBase.objects.filter(enabled=True)
        ads_enabled.update(start_showing=now(),
                           stop_showing=max_dt)
        ads_disabled = AdBase.objects.filter(enabled=False)
        ads_disabled.update(start_showing=now(),
                            stop_showing=now())

    def backwards(self, orm):
        "Write your backwards methods here."
        AdBase = orm['adzone.adbase']
        ads_enabled = AdBase.objects.filter(start_showing__lte=now(),
                                            stop_showing__gte=now())
        ads_enabled.update(enabled=True)
        ads_disabled = (AdBase.objects.filter(start_showing__gte=now()) |
                        AdBase.objects.filter(stop_showing__lte=now()))
        ads_disabled.update(enabled=False)

    models = {
        'adzone.adbase': {
            'Meta': {'object_name': 'AdBase'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adzone.Advertiser']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adzone.AdCategory']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'since': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_showing': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'stop_showing': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(9999, 12, 31, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adzone.AdZone']"})
        },
        'adzone.adcategory': {
            'Meta': {'ordering': "('title',)", 'object_name': 'AdCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'adzone.adclick': {
            'Meta': {'object_name': 'AdClick'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adzone.AdBase']"}),
            'click_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'adzone.adimpression': {
            'Meta': {'object_name': 'AdImpression'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adzone.AdBase']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impression_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'adzone.advertiser': {
            'Meta': {'ordering': "('company_name',)", 'object_name': 'Advertiser'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'adzone.adzone': {
            'Meta': {'ordering': "('title',)", 'object_name': 'AdZone'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'adzone.bannerad': {
            'Meta': {'object_name': 'BannerAd', '_ormbases': ['adzone.AdBase']},
            'adbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['adzone.AdBase']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'adzone.textad': {
            'Meta': {'object_name': 'TextAd', '_ormbases': ['adzone.AdBase']},
            'adbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['adzone.AdBase']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['adzone']
    symmetrical = True