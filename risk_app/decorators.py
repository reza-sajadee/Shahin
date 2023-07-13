from django.core.exceptions import PermissionDenied
from .models import RiskProfile
from profile_app.models import Profile
def user_is_dabir(function):
    def wrap(self, *args, **kwargs):
        print('noooooooooooo')
        if self.request.user.is_superuser:
            print('user is admin')
            return function(self, *args, **kwargs)
        try:
            risk_profile = RiskProfile.objects.all()[0]
        except:
            print('user is rased erore')
            raise PermissionDenied
        
            
        if risk_profile.committeeRisk.dabir == Profile.objects.filter(user =self.request.user)[0]   :
            print('user is dabir ')
            return function(self, *args, **kwargs)
        else:
            
            print('user is not dabir ' , risk_profile.committeeRisk.dabir.user ,Profile.objects.filter(user =self.request.user) )
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap