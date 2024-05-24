from user_app.models import settings
from .models import *

def kycver(request):
    try:
      active =   Kycverification.objects.filter(user=request.user).first
    except:
       Kycverification.DoesNotExist
       active = None
    return {'active':active}



def setupinfo(request):
   sinfo = setup.objects.filter().first
   return {'sinfo':sinfo}