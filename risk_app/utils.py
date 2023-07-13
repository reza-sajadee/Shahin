from .models import RiskProfile
from profile_app.models import Profile

def is_dabir(self):
    if self.request.user.is_superuser:
            
            return True
    risk_profile = RiskProfile.objects.all()
    
    if(len(risk_profile) ==0 ):
        return False
    else:
        risk_profile = risk_profile[0]
    try:
        if risk_profile.committeeRisk.dabir == Profile.objects.filter(user =self.request.user)[0]  :
            return True
        else:
            return False
    except:
        return False
    

def avrage(elements):
    leanght_of_elements = len(elements)
    if(leanght_of_elements == 0):
        
        return 0
    sum_of_elements = 0
    for element in elements:
        sum_of_elements+=element
    return sum_of_elements/leanght_of_elements

def std(elements):
    leanght_of_elements = len(elements)
    if(leanght_of_elements == 0):
        return 0
    avrage_of_elements = avrage(elements)
    sum_of_elements = 0
    for element in elements :
        sum_of_elements +=(element - avrage_of_elements) ** 2
    return (float(sum_of_elements)/float(leanght_of_elements))**(0.5)