import datetime

from django.contrib.sites.models import Site

from django.db import models
try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.datetime.now


class AdManager(models.Manager):
    """ A Custom Manager for ads """

    def get_random_ad(self, ad_zone, ad_category=None):
        """
        Returns a random advert that belongs for the specified ``ad_category``
        and ``ad_zone``.
        If ``ad_category`` is None, the ad will be category independent.
        """
        qs = self.get_queryset().filter(start_showing__lte=now(),
                                         stop_showing__gte=now(),
                                         zone__slug=ad_zone,
                                         sites=Site.objects.get_current().pk
                                         ).select_related('textad',
                                                          'bannerad')
        if ad_category:
            qs = qs.filter(category__slug=ad_category)
        try:
            ad = qs.order_by('?')[0]
        except IndexError:
            return None
        return ad
