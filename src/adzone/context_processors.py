def get_source_ip(request):
    if request.META.has_key('REMOTE_ADDR'):
        return {'from_ip': request.META.get('REMOTE_ADDR')}
    else:
        return {}
