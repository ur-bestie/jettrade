from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.utils.safestring import mark_safe
# Create your views here.
def index(request):
    return render(request,'home/index.html')

@login_required
def userdash(request):
    x = setup.objects.filter().first
    return render(request,'user/dashboard/user.html',locals())

def register(request):
     if request.method == 'POST':  
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')  
        if password == password2:
          if CustomUser.objects.filter(username=username).exists():
             messages.error(request,'Username Already Exists')
             return redirect('/register')
          elif CustomUser.objects.filter(email=email).exists():
            messages.error(request,'Email already in use')
            return redirect('/register')
          else:
             hashed_password = make_password(password)
             user = CustomUser(first_name=first_name,last_name=last_name,username=username, email=email, password=hashed_password)
             user.save()
             return redirect('emailverification', username=request.POST.get('username'))
        else:    
         messages.error(request,'password not the same')
         return redirect('/signup')  
     else:
        return render(request,'user/auth/register.html')

def user_login(request): 
   if request.method == 'POST':
       email = request.POST.get('email')
       password = request.POST.get('password')
       

       user = authenticate(request, email=email, password=password)
       if user is not None:
          login(request, user)
          return redirect('/user')
       else:
          messages.error(request,'Email or password not correct')
          return redirect('/login')
       
   return render(request,'user/auth/login.html')

def logout(request):
   auth.logout(request)
   return redirect('/')

def emailverification(request, username):
    user = request.user
    user = get_user_model().objects.get(username=username)
    uopt = otp.objects.filter(user=user).last()

    if request.method == 'POST':
        if uopt.code1 == request.POST.get('code1'):
          if uopt.exp > timezone.now():
            uopt.verify = True
            uopt.save()
            messages.success(request,'Email verification is successful Login Now')
            subject = "Verification completed"
            message = f"""
 Hi {user.username}, your email has been verified you can now login https://jettrade.com/login.
https://Jettrade.com.ng .Allright reserve 2024 
"""
            sender = "test@kcls-swift.com"
            receiver = [user.email, ]


            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            return redirect('login')
          else:
            messages.error(request, 'This otp have expired, get a new otp')
          return redirect('/resend_otp')  
        else:
          messages.error(request, 'Invalid otp,Enter a valid otp')
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
     return render(request,'user/auth/emailverification.html')

def resend_otp(request):
   
   if request.method == 'POST':
      emailch = request.POST.get('email')
      if get_user_model().objects.filter(email = emailch).exists():
            user = get_user_model().objects.get(email=emailch)
            otpc = otp.objects.create(user=user, exp=timezone.now() + timezone.timedelta(minutes=5))

            #email  
            otpc  = otp.objects.filter(user=user).last()
            subject = "New otp"
            message = f"""
 Hi {user.username},your new otp is {otpc.code1} this codes expires in 5 minute. http://127.0.0.1:8000/emailverification/{user.username}.
https://Jettrade.com.ng .Allright reserve 2024
"""
            sender = "test@kcls-swift.com"
            receiver = [emailch, ]


            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )


            return redirect('emailverification', username=user.username)
      else:
         messages.error(request,'Email Not Available, Please Enter A Registered Email')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'user/auth/resend_otp.html')

def crypto(request):
    return render(request,'user/dashboard/crypto.html')

def giftcard(request):
    return render(request,'user/dashboard/giftcard.html')

def cryptobuy(request):
    x = coins.objects.all()
    sinfo = setup.objects.filter().first
    pg = paymentmethod.objects.all()

    if request.method == 'POST':
       user = request.user
       amount = request.POST.get('amount')
       rate_naira = request.POST.get('rate_naira')
       receiving_address = request.POST.get('receiving_address')
       payment = request.POST.get('payment')
       payment_id = request.POST.get('p_id')
       co_id = request.POST.get('c_id')
      
       x_id = coins.objects.get(pk=co_id)
       pg_id = paymentmethod.objects.get(pk=payment_id)

       sv = buying_history.objects.create(
          user=user,coin=x_id,amount=amount,rate_naira=rate_naira,receiving_address=receiving_address,payment=payment,paymentmethod=pg_id
       )
       sv.save()
       #email sell 
       subject = "Crypto Buy"
       message = f"""
 Hi {user.username}, you have successfully placed an order to buy crypto that worth  {payment} please make sure you pay the amount purchased follow the information provided your the invoice page to complate this transaction.
https://Jettrade.com.ng .Allright reserve 2024
"""
       sender = "test@kcls-swift.com"
       receiver = [user.email, ]


       send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
       messages.success(request,'Crypto purchase is succesful make sure you complete your payment')
       buying_history_id = sv.id
       return redirect('paymentinfo',buying_history_id=buying_history_id)
    else:
     return render(request,'user/dashboard/cryptobuy.html',locals())

def passreset(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the old password matches
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('passreset')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('passreset')

        # Update the password
        user.set_password(new_password)
        user.save()
        
        # Update session authentication hash
        update_session_auth_hash(request, user)
        #email password change 
        subject = "Password change"
        message = f"""
 Hi {user.username}, you have successfully changed your password.
https://Jettrade.com.ng .Allright reserve 2024
"""
        sender = "test@kcls-swift.com"
        receiver = [user.email, ]


        send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
        messages.success(request, 'Password updated successfully.')
        return redirect('passreset')
    
    return render(request,'user/auth/passreset.html')



def profile(request):
   x = get_user_model().objects.filter()
   return render(request,'user/dashboard/profile.html',locals())



def kyc(request):
   user=request.user
   if request.method == 'POST':
        # Retrieve form data from request.POST
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        nationality = request.POST.get('nationality')
        zip_code = request.POST.get('zip_code')
        id_type = request.POST.get('id_type')
        gender = request.POST.get('gender')
        id_proof = request.FILES.get('id_proof')
        selfie = request.FILES.get('selfie')
        # Process other form fields similarly

        # Now you can save the data to the database or perform any other necessary actions
        # For demonstration purposes, let's assume you're saving the data to the database
        # You would need to adjust this based on your actual models
        Kycverification.objects.create(
            user=user,
            phone=phone,
            date_of_birth=date_of_birth,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            nationality=nationality,
            zip_code=zip_code,
            id_type=id_type,
            gender=gender,
            id_proof=id_proof,
            selfie=selfie,
            # Save other form fields similarly
        )
        #email kyc verification 
        subject = "Kyc Submition"
        message = f"""
 Hi {user.username}, you have successfully submited your kyc, Our team will review your kyc and you will be notified if approved or rejected.
https://Jettrade.com.ng .Allright reserve 2024
"""
        sender = "test@kcls-swift.com"
        receiver = [user.email, ]


        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )

        messages.success(request,'kyc is updated successfully')
        return redirect('user')  
   return render(request,'user/dashboard/kyc.html')


def cryptosell(request):
    x = coins.objects.all()
    sinfo = setup.objects.filter().first
    

    if request.method == 'POST':
       user = request.user
       amount = request.POST.get('amount')
       rate_naira = request.POST.get('rate_naira')
       payment = request.POST.get('payment')
       payment_info = request.POST.get('payment_info')
       co_id = request.POST.get('c_id')
      
       x_id = coins.objects.get(pk=co_id)
       
       sv = selling_history.objects.create(
          user=user,coin=x_id,amount=amount,rate_naira=rate_naira,payment=payment,payment_info=payment_info
       )
       sv.save()
       messages.success(request,'you have made a new sale')
       #email sell 
      #  subject = "Crypto sell"
      #  message = f"""

      #                Hi {user.username}, you have successfully sold your crypto please make sure you deposit the amount sold follow the information provided in your invoice page

      #                https://Jettrade.com.ng .Allright reserve 2024

      #                """
      #  sender = "test@kcls-swift.com"
      #  receiver = [user.email, ]


      #  send_mail(
      #       subject,
      #       message,
      #       sender,
      #       receiver,
      #       fail_silently=False,
      #   )
       selling_history_id = sv.id
       return redirect('cryptosellpaymentinfo',selling_history_id=selling_history_id)
    else:
     return render(request,'user/dashboard/cryptosell.html',locals())



def sellinginvoice(request, selling_history_id):
    x = selling_history.objects.get(id= selling_history_id)
    return render(request,'user/dashboard/sellinginvoice.html', {'x': x})


def selling_hist(request):
   user = request.user
   try:
    x = selling_history.objects.filter(user=user)
   except: 
      selling_history.DoesNotExist
      x = None
   return render(request,'user/dashboard/selling_history.html',locals())


def buyinginvoice(request, buying_history_id):
   x = buying_history.objects.get(id=buying_history_id)
   return render(request,'user/dashboard/buyinginvoice.html',locals())


def buying_hist(request):
   user = request.user
   try:
    x = buying_history.objects.filter(user=user)
   except: 
      buying_history.DoesNotExist
      x = None
   return render(request,'user/dashboard/buying_history.html',locals())




def giftcardbuy(request):
   x = giftcards.objects.all()
   sinfo = setup.objects.filter().first
   pg = paymentmethod.objects.all()
   if request.method == 'POST':
       user = request.user
       amount = request.POST.get('amount')
       rate_naira = request.POST.get('rate_naira')
       recipient_name = request.POST.get('recipient_name')
       recipient_whatsapp = request.POST.get('recipient_whatsapp')
       payment = request.POST.get('payment')
       payment_id = request.POST.get('p_id')
       co_id = request.POST.get('c_id')
      
       x_id = giftcards.objects.get(pk=co_id)
       pg_id = paymentmethod.objects.get(pk=payment_id)

       sv = giftcardbuying_history.objects.create(
          user=user,giftcard=x_id,amount=amount,rate_naira=rate_naira,recipient_name=recipient_name,recipient_whatsapp=recipient_whatsapp,payment=payment,paymentmethod=pg_id
       )
       sv.save()
       #email sell 
       subject = "Crypto Buy"
       message = f""" 
 Hi {user.username}, you have successfully placed an order to buy giftcard worth {payment} please make sure you complate your payment, follow the information provided in your invoice page to complete this transaction.
https://Jettrade.com.ng .Allright reserve 2024
"""
                                
       sender = "test@kcls-swift.com"
       receiver = [user.email, ]


       send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
       messages.success(request,'Crypto purchase is succesful make sure you complete your payment')
       buying_history_id = sv.id
       return redirect('giftcardbuypaymentinfo',buying_history_id=buying_history_id)
   else:
    return render(request,'user/dashboard/giftcardbuy.html',locals())


def giftcardbuyinginvoice(request, buying_history_id):
   
   x = giftcardbuying_history.objects.get(id=buying_history_id)
   return render(request,'user/dashboard/giftcardbuyinginvoice.html',locals())


def giftcardbuying_hist(request):
   user = request.user
   try:
    x = giftcardbuying_history.objects.filter(user=user)
   except: 
      giftcardbuying_history.DoesNotExist
      x = None
   return render(request,'user/dashboard/giftcardbuying_hist.html',locals())


def paymentinfo(request, buying_history_id):
   x = buying_history.objects.get(id=buying_history_id)
   return render(request,'user/dashboard/paymentinfo.html',locals())

def cryptobuyconfirm(request, buying_history_id):
   x = buying_history.objects.get(id=buying_history_id)
   s = setup.objects.first()
   ss = s.siteemail
   #email sell 
   subject = "Confirm payment"
   message = f""" 
 Hello jettrade, you have a new crypto payment to confirm from {x.user.first_name}.
payment amount {x.payment} Business type crypto Buy.
https://Jettrade.com.ng .Allright reserve 2024
"""
                           
   sender = "test@kcls-swift.com"
   receiver = [ss, ]


   send_mail(
      subject,
      message,
      sender,
      receiver,
      fail_silently=False,
   )
   return redirect('buyinginvoice',buying_history_id=buying_history_id)



def cryptobuycancel(request, buying_history_id):
   user=request.user
   x = buying_history.objects.get(id=buying_history_id)
   x.delete()
   #email sell 
   subject = "canceled Transaction"
   message = f""" 
  you have successfully canceled the purchase
https://Jettrade.com.ng .Allright reserve 2024
"""
                           
   sender = "test@kcls-swift.com"
   receiver = [user.email, ]


   send_mail(
      subject,
      message,
      sender,
      receiver,
      fail_silently=False,
   )
   return redirect('cryptobuy')




def cryptosellpaymentinfo(request, selling_history_id):
   x = selling_history.objects.get(id=selling_history_id)
   return render(request,'user/dashboard/cryptosellpaymentinfo.html',locals())

def cryptosellconfirm(request, selling_history_id):
   x = selling_history.objects.get(id=selling_history_id)
   s = setup.objects.first()
   ss = s.siteemail
   #email sell 
   subject = "Confirm payment"
   message = f""" 
 Hello jettrade, you have a new crypto payment to confirm from {x.user.first_name}.
payment amount {x.payment} Business type crypto sell.
https://Jettrade.com.ng .Allright reserve 2024
"""
                           
   sender = "test@kcls-swift.com"
   receiver = [ss, ]


   send_mail(
      subject,
      message,
      sender,
      receiver,
      fail_silently=False,
   )
   return redirect('sellinginvoice',selling_history_id=selling_history_id)



def cryptosellcancel(request, selling_history_id):
   user=request.user
   x = selling_history.objects.get(id=selling_history_id)
   x.delete()
   #email sell 
   subject = "Canceled Transaction"
   message = f""" 
  you have successfully canceled the sell
https://Jettrade.com.ng .Allright reserve 2024
"""
                           
   sender = "test@kcls-swift.com"
   receiver = [user.email, ]


   send_mail(
      subject,
      message,
      sender,
      receiver,
      fail_silently=False,
   )
   return redirect('cryptosell')





def giftcardbuypaymentinfo(request, buying_history_id):
   x = giftcardbuying_history.objects.get(id=buying_history_id)
   return render(request,'user/dashboard/giftcardbuypaymentinfo.html',locals())

def giftcardbuyconfirm(request, buying_history_id):
   x = giftcardbuying_history.objects.get(id=buying_history_id)
   s = setup.objects.first()
   ss = s.siteemail
   #email sell 
   subject = "Confirm payment"
   message = f""" 
 Hello jettrade, you have a new giftcard payment to confirm from {x.user.first_name}.
payment amount {x.payment} Business type giftcard buy.
https://Jettrade.com.ng .Allright reserve 2024
"""
                           
   sender = "test@kcls-swift.com"
   receiver = [ss, ]


   send_mail(
      subject,
      message,
      sender,
      receiver,
      fail_silently=False,
   )
   return redirect('giftcardbuyinginvoice',buying_history_id=buying_history_id)



def giftcardbuycancel(request, buying_history_id):
   user=request.user
   x = giftcardbuying_history.objects.get(id=buying_history_id)
   x.delete()
   #email sell 
   subject = "Canceled Transaction"
   message = f""" 
  you have successfully canceled the purchase.
https://Jettrade.com.ng .Allright reserve 2024
"""
                           
   sender = "test@kcls-swift.com"
   receiver = [user.email, ]


   send_mail(
      subject,
      message,
      sender,
      receiver,
      fail_silently=False,
   )
   return redirect('giftcardbuy')


def forgetpassword(request):
   return render(request,'user/auth/forgetpassword.html')



#NR6UJ8XXW6LHTERKMZXNGDVF