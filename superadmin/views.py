from django.shortcuts import render, redirect
from user_app.models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@staff_member_required
def dashboard(request):
    return render(request,'admin_temp/index.html')

@staff_member_required
def userkyc(request):
    x = Kycverification.objects.all()
    kcy_t = len(x)
    if request.method == 'POST':
       kycid = request.POST.get('kycid')
       sv = Kycverification.objects.get(pk=kycid)
       sv.status = True
       sv.save()
       #email sell
       subject = "Kyc"
       message = f"""
 Hello {sv.user.username}, your kyc has been approved you can now buy or sell in the jettrade trading platform.
https://Jettrade.com.ng .Allright reserve 2024
"""

       sender = "test@kcls-swift.com"
       receiver = [sv.user.email, ]


       send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
       messages.success(request,'kyc approved successfully')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
     return render(request,'admin_temp/userkyc.html', locals())

@staff_member_required
def keycreject(request, id):
   x = Kycverification.objects.get(id=id)
   x.delete()
   #email sell
   subject = "Kyc"
   message = f"""
 Hello {x.user.username}, your kyc has been rejected you can not buy or sell in the jettrade trading platform please do submit a valid information.
https://Jettrade.com.ng .Allright reserve 2024
"""

   sender = "test@kcls-swift.com"
   receiver = [x.user.email, ]


   send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
   messages.success(request,'kyc Rejected successfully')
   return redirect('/superadmin/userkyc')

@staff_member_required
def userkycview(request, id):
   x = Kycverification.objects.get(id=id)
   return render(request,'admin_temp/userkycview.html', locals())

@staff_member_required
def trancryptobuy(request):
   x = buying_history.objects.all()
   t_tal = len(buying_history.objects.all())
   if request.method == 'POST':
      u_id = request.POST.get('u_id')
      sv = buying_history.objects.get(id=u_id)
      sv.status = True
      sv.save()
      #email sell
      subject = "Crypto Transaction"
      message = f"""
 Hello {sv.user.username}, your Transaction on crypto purchase has been approved.
https://Jettrade.com.ng .Allright reserve 2024
"""

      sender = "test@kcls-swift.com"
      receiver = [sv.user.email, ]


      send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
      messages.success(request,'Payment has been approved')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'admin_temp/trancryptobuy.html', locals())

@staff_member_required
def trancryptosell(request):
   x = selling_history.objects.all()
   t_tal = len(selling_history.objects.all())
   if request.method == 'POST':
      u_id = request.POST.get('u_id')
      sv = selling_history.objects.get(id=u_id)
      sv.status = True
      sv.save()
      #email sell
      subject = "Crypto transaction"
      message = f"""
 Hello {sv.user.username}, the crypto you sold has been approved.
https://Jettrade.com.ng .Allright reserve 2024
"""

      sender = "test@kcls-swift.com"
      receiver = [sv.user.email, ]


      send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
      messages.success(request,'Payment has been approved')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'admin_temp/trancryptosell.html', locals())

@staff_member_required
def trangiftbuy(request):
   x = giftcardbuying_history.objects.all()
   t_tal = len(giftcardbuying_history.objects.all())
   if request.method == 'POST':
      u_id = request.POST.get('u_id')
      sv = giftcardbuying_history.objects.get(id=u_id)
      sv.status = True
      sv.save()
      #email sell
      subject = "Giftcard transaction"
      message = f"""
 Hello {sv.user.username}, your Giftcard purchase has been approved.
https://Jettrade.com.ng .Allright reserve 2024
"""

      sender = "test@kcls-swift.com"
      receiver = [sv.user.email, ]


      send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
      messages.success(request,'Payment has been approved')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'admin_temp/trangiftbuy.html', locals())

@staff_member_required
def trancryptobuydelete(request, id):
   x = buying_history.objects.get(id=id)
   x.delete()
   #email sell
   subject = "Crypto transaction"
   message = f"""
 Hello {x.user.username}, your crypto purchase has been rejected please contact the admin.
https://Jettrade.com.ng .Allright reserve 2024
"""

   sender = "test@kcls-swift.com"
   receiver = [x.user.email, ]


   send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
   messages.success(request,'rejected successfully')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def trancryptoselldelete(request, id):
   x = selling_history.objects.get(id=id)
   x.delete()
   #email sell
   subject = "Crypto transaction"
   message = f"""
 Hello {x.user.username}, The crypto you sold has been rejected please contact the admin.
https://Jettrade.com.ng .Allright reserve 2024
"""

   sender = "test@kcls-swift.com"
   receiver = [x.user.email, ]


   send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
   messages.success(request,'rejected successfully')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def trangiftbuydelete(request, id):
   x = giftcardbuying_history.objects.get(id=id)
   x.delete()
   #email sell
   subject = "Giftcard transaction"
   message = f"""
 Hello {x.user.username}, your Giftcard purchase has been rejected please contact the admin.
https://Jettrade.com.ng .Allright reserve 2024
"""

   sender = "test@kcls-swift.com"
   receiver = [x.user.email, ]


   send_mail(
         subject,
         message,
         sender,
         receiver,
         fail_silently=False,
      )
   messages.success(request,'rejected successfully')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def userpage(request):
   return render(request,'admin_temp/userpage.html', locals())



@staff_member_required
def cryptoproduct(request):
   x = coins.objects.all()
   if request.method == 'POST':
      name = request.POST.get('name')
      logo = request.FILES.get('logo')
      buying_quantity = request.POST.get('buying_quantity')
      selling_quantity = request.POST.get('selling_quantity')
      wallet_address = request.POST.get('wallet_address')
      if coins.objects.filter(name=name).exists():
       messages.error(request,'Coin Already Exists')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
         sv = coins.objects.create(name=name,logo=logo,wallet_address=wallet_address,buying_quantity=buying_quantity,selling_quantity=selling_quantity)
         sv.save()
         messages.success(request,'Coin is  added successfully')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'admin_temp/cryptoproduct.html',locals())



@staff_member_required
def cryptoproductdel(request, id):
   x = coins.objects.get(id=id)
   x.delete()
   messages.success(request,'Coin deleted successfully')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def cryptoproductedit(request, id):
   x = coins.objects.get(id=id)
   if request.method == 'POST':
      name = request.POST.get('name')
      logo = request.FILES.get('logo')
      wallet_address = request.POST.get('wallet_address')
      buying_quantity = request.POST.get('buying_quantity')
      selling_quantity = request.POST.get('selling_quantity')

      x.name = name
      x.logo = logo
      x.wallet_address=wallet_address
      x.buying_quantity=buying_quantity
      x.selling_quantity = selling_quantity
      x.save()
      messages.success(request,'coin update is successful')
      return redirect('cryptoproduct')
   else:
    return render(request,'admin_temp/cryptoproductedit.html',locals())



@staff_member_required
def giftcardproduct(request):
   x = giftcards.objects.all()
   if request.method == 'POST':
      name = request.POST.get('name')
      logo = request.FILES.get('logo')
      if giftcards.objects.filter(name=name).exists():
       messages.error(request,'Giftcard Already Exists')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
         sv = giftcards.objects.create(name=name,logo=logo)
         sv.save()
         messages.success(request,'Giftcard is added successfully')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'admin_temp/giftcardproduct.html',locals())


@staff_member_required
def giftcardproductdel(request, id):
   x = giftcards.objects.get(id=id)
   x.delete()
   messages.success(request,'Giftcard is deleted successfully')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def giftcardproductedit(request, id):
   x = giftcards.objects.get(id=id)
   if request.method == 'POST':
      name = request.POST.get('name')
      logo = request.FILES.get('logo')

      x.name = name
      x.logo = logo
      x.save()
      messages.success(request,'Giftcard update is successful')
      return redirect('giftcardproduct')
   else:
    return render(request,'admin_temp/giftcardproductedit.html',locals())



@staff_member_required
def passwordchange(request):
   if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the old password matches
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('passwordchange')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('passwordchange')

        # Update the password
        user.set_password(new_password)
        user.save()

        # Update session authentication hash
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated successfully.')
        return redirect('passwordchange')

   return render(request,'admin_temp/passwordchange.html')



@staff_member_required
def adminsettings(request):
   x = setup.objects.filter().first
   if request.method == 'POST':
      crypto_buying_rate = request.POST.get('crypto_buying_rate')
      crypto_selling_rate = request.POST.get('crypto_selling_rate')
      giftcard_buying_rate = request.POST.get('giftcard_buying_rate')
      giftcard_selling_rate = request.POST.get('giftcard_selling_rate')
      siteemail = request.POST.get('siteemail')
      sid = request.POST.get('sid')

      ids = setup.objects.get(pk=sid)
      ids.crypto_buying_rate = crypto_buying_rate
      ids.crypto_selling_rate = crypto_selling_rate
      ids.giftcard_buying_rate = giftcard_buying_rate
      ids.giftcard_selling_rate = giftcard_selling_rate
      ids.siteemail = siteemail
      ids.save()
      messages.success(request,'site settings is successfully')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

   else:
    return render(request,'admin_temp/adminsettings.html',locals())



def deposit(request):
   x = balance_history.objects.all()
   t_tal = len(balance_history.objects.all())
   if request.method == 'POST':
      u_id = request.POST.get('u_id')
      b_id = request.POST.get('b_id')
      sv = balance_history.objects.get(id=u_id)
      bid = balance.objects.get(id=b_id)
      amount = sv.amount
      sv.status = True
      bid.amount += float(amount)
      bid.save()
      sv.save()
      #email sell
      subject = "Deposit transaction"
      message = f"""
 Hello {sv.balance.user.username}, your Deposit has been approved.
https://Jettrade.com.ng .Allright reserve 2024
"""

      sender = "test@kcls-swift.com"
      receiver = [sv.balance.user.email, ]


      # send_mail(
      #    subject,
      #    message,
      #    sender,
      #    receiver,
      #    fail_silently=False,
      # )
      messages.success(request,'Payment has been approved')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'admin_temp/deposit.html',locals())