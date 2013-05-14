from django.db import models


class AdManager(models.Manager):
    """ A Custom Manager for ads """

    def get_random_ad(self, ad_zone, ad_category=None):
        """
        Returns a random advert that belongs for the specified ``ad_category``
        and ``ad_zone``.
        If ``ad_category`` is None, the ad will be category independent.
        """
        try:
            if ad_category:
                ad = self.get_query_set().filter(
                    enabled=True,
                    category__slug=ad_category,
                    zone__slug=ad_zone
                ).order_by('?')[0]
            else:
                ad = self.get_query_set().filter(
                    zone__slug=ad_zone).order_by('?')[0]
        except IndexError:
            return None
        return ad
