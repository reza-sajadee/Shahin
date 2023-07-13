from django.core.exceptions import PermissionDenied
from .models import TypeMomayezi
from profile_app.models import Profile
def user_is_modir(function):
    def wrap(self, *args, **kwargs):
        if self.request.user.is_superuser:
            print('user is admin')
            return function(self, *args, **kwargs)
        try:
            type_modir = TypeMomayezi.objects.all()[0]
        except:
            print('user is rased erore')
            raise PermissionDenied
        
            
        if type_modir.modir == Profile.objects.filter(user =self.request.user)[0]   :
            print('user is modir ')
            return function(self, *args, **kwargs)
        else:
            
            print('user is not modir ' , type_modir.modir ,Profile.objects.filter(user =self.request.user) )
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap