
#put it to your app/shared/decorators.py and than import when required

from django.core.exceptions import PermissionDenied

def staff_only(function):
    """
    Limit view to superusers only.

    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """
    def _inner(self, *args, **kwargs):
        if not self.request.user.is_staff :
            raise PermissionDenied
        return function(self, *args, **kwargs)
    return _inner


def SuperUser_only(function):
    """
    Limit view to superusers only.

    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """
    def _inner(self, *args, **kwargs):

        if  not self.request.user.is_superuser:
            raise PermissionDenied
        return function(self, *args, **kwargs)
    return _inner


