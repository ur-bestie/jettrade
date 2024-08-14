import requests
import logging
from django.http import JsonResponse
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
from django.views import View
from django.conf import settings
import json
from django.urls import reverse
from django.templatetags.static import static

# Create your views here.
def index(request):
    return render(request,'home/index.html')

@login_required
def userdash(request):
     b = balance.objects.filter(user=request.user).first
     x = recent_activity.objects.filter(user=request.user).order_by('-date')[:3]
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

def addfunds(request):
    user = request.user
    user_id = user.id

    bl, created = balance.objects.get_or_create(user=user)

    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except (ValueError, TypeError):
            return render(request, 'user/dashboard/addfunds.html', {'error': 'Invalid amount.'})

        est = amount * 0.017 
        pay = amount + est
        
        balance_history_obj = balance_history.objects.create(balance=bl,payamount=pay, amount=amount)
        # Get the ID of the newly created balance_history object
        x = balance_history_obj.id
        # Redirect to the payment page with the correct parameter name
        return redirect(reverse('payment', kwargs={'id': x}))
    else:
         return render(request, 'user/dashboard/addfunds.html')


@login_required
def withdraw(request):
    user = request.user
    user_id = user.id
    x = bankdetails.objects.all()
    bl = balance.objects.filter(user_id=user_id).first()
    
    if request.method == 'POST':
        bank_id = request.POST.get('bank_id')
        name = request.POST.get('name')
        account_number = request.POST.get('account_number')
        amt = request.POST.get('amount')
        bd = bankdetails.objects.get(pk=bank_id)
        amount = int(amt)

        # API Call to Flutterwave
        # url = "https://api.flutterwave.com/v3/transfers"
        # headers = {
        #     "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",  # Use your secret key from settings
        #     "Content-Type": "application/json"
        # }
        # data = {
        #     "account_bank": bank_id,  # Assuming 'bank_code' is a field in bankdetails
        #     "account_number": account_number,
        #     "amount": amount,
        #     "narration": "Withdrawal",
        #     "currency": "NGN",
        #     "reference": f"withdrawal_{user_id}",
        #     "callback_url": "https://yourwebsite.com/callback-url",  # Replace with your callback URL
        #     "debit_currency": "NGN"
        # }

        # response = requests.post(url, headers=headers, json=data)
        
        # if response.status_code == 200:
        #     # Handle successful transfer response
        #     print("Transfer successful:", response.json())
            # Optionally, update the withd_his object with API response data
            
            # Create withdrawal history record
        if bl.amount < amount:
               messages.error(request,'amount is greater than your balance')
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
                x = withd_his.objects.create(user=user, bank=bd, name=name,account_number=account_number, amount=amount)
                sid = x.id
                ra = recent_activity.objects.create(user=request.user, name='withdrawal', amount=amount, a_id=sid)
            
            # Create recent activity record
        

            # x.api_response = response.json()  # Example field, add to your model if necessary
            # x.save()
        return redirect('activities')
        # else:
        #     # Handle failed transfer response
        #     print("Transfer failed:", response.status_code, response.text)
        #     # Optionally, handle the error (e.g., show a message to the user)
        
        # return redirect('withdraw')

    return render(request, 'user/dashboard/withdraw.html', locals())
    
def payment(request, id):
    user = request.user
    x = balance_history.objects.get(pk=id)
    return render(request,'user/dashboard/payment.html',locals())

def confirmbankdeposit(request):
    
     return render(request,'user/dashboard/test.html',locals())

def giftcard(request):
    return render(request,'user/dashboard/giftcard.html')

def cryptobuy(request):
    x = coins.objects.all()
    sinfo = setup.objects.filter().first
    pg = paymentmethod.objects.all()
    
    user_id = request.user.id  # Get the user ID
    bl = balance.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
       user = request.user
       amount = request.POST.get('amount')
       rate_naira = request.POST.get('rate_naira')
       receiving_address = request.POST.get('receiving_address')
       payment = request.POST.get('payment')
       payment_id = request.POST.get('p_id')
       co_id = request.POST.get('c_id')
      
       x_id = coins.objects.get(pk=co_id)
       pg_id = paymentmethod.objects.get(pk=1)
       
       if float(amount) > bl.amount:
         messages.error(request,'Amount is greater than your main balance')
         return redirect('/cryptobuy')
       else:
        bl.amount -= float(amount)
        bl.save()
        sv = buying_history.objects.create(
          user=user,coin=x_id,amount=amount,rate_naira=rate_naira,receiving_address=receiving_address,payment=payment,paymentmethod=pg_id
       )
        sid = sv.id
        sv.status = True
        ra = recent_activity.objects.create(user=request.user,name='crypto buy',amount=amount,a_id=sid) 
        sv.save()
       #email sell 
       subject = "Crypto Buy"
       message = f"""
 Hi {user.username}, you have successfully placed an order to buy crypto that worth  {payment} please make sure you pay the amount purchased follow the information provided your the invoice page to complate this transaction.
https://Jettrade.com.ng .Allright reserve 2024
"""
       sender = "test@kcls-swift.com"
       receiver = [user.email, ]


    #    send_mail(
    #         subject,
    #         message,
    #         sender,
    #         receiver,
    #         fail_silently=False,
    #     )
       messages.success(request,'Crypto purchase is succesful')
       buying_history_id = sv.id
       return redirect('cryptobuyconfirm',buying_history_id=buying_history_id)
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
       sid = sv.id
       ra = recent_activity.objects.create(user=request.user,name='crypto sell',img=x_id.logo,amount=amount,a_id=sid) 
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
       return redirect('activities')
    else:
     return render(request,'user/dashboard/cryptosell.html',locals())



def sellinginvoice(request, selling_history_id):
    x = selling_history.objects.get(id= selling_history_id)
    return render(request,'user/dashboard/sellinginvoice.html', {'x': x})


def airtime_his(request, id):
   user = request.user
   x = airtime_Transaction.objects.get(pk=id)
   return render(request,'user/dashboard/airtime_his.html',locals())


def buyinginvoice(request, buying_history_id):
   x = buying_history.objects.get(id=buying_history_id)
   return render(request,'user/dashboard/buyinginvoice.html',locals())


def data_his(request, id):
   x = datap_history.objects.get(pk=id)
   return render(request,'user/dashboard/data_his.html',locals())


def marketplace(request):
   return render(request,'user/dashboard/marketplace.html',locals())


def giftcardbuy(request):
   x = giftcards.objects.all()
   sinfo = setup.objects.filter().first
   pg = paymentmethod.objects.all()
   user_id = request.user.id  # Get the user ID
   bl = balance.objects.filter(user_id=user_id).first()
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
       pg_id = paymentmethod.objects.get(pk=1)
      
       if float(amount) > bl.amount:
         messages.error(request,'Amount is greater than your main balance')
         return redirect('/giftcardbuy')
       else:
        bl.amount -= float(amount)
        bl.save()
       print(x_id.id)
       sv = giftcardbuying_history.objects.create(
          user=user,giftcard=x_id,amount=amount,rate_naira=rate_naira,recipient_name=recipient_name,recipient_whatsapp=recipient_whatsapp,payment=payment,paymentmethod=pg_id
       )
       sid = sv.id
       ra = recent_activity.objects.create(user=request.user,name='Giftcard buy',img=x_id.logo,amount=amount,a_id=sid) 
       sv.save()
       #email sell 
       subject = "Giftcard Purchase"
       message = f""" 
 Hi {user.username}, you have successfully placed an order to buy giftcard worth {payment} please make sure you complate your payment, follow the information provided in your invoice page to complete this transaction.
https://Jettrade.com.ng .Allright reserve 2024
"""
                                
       sender = "test@kcls-swift.com"
       receiver = [user.email, ]


      #  send_mail(
      #       subject,
      #       message,
      #       sender,
      #       receiver,
      #       fail_silently=False,
      #   )
       messages.success(request,'Crypto purchase is succesful make sure you complete your payment')
       buying_history_id = sv.id
       return redirect('activities')
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


def activities(request):
   x = recent_activity.objects.all()
   return render(request,'user/dashboard/activities.html',locals())


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


#    send_mail(
#       subject,
#       message,
#       sender,
#       receiver,
#       fail_silently=False,
#    )
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
   return redirect('/cryptobuy')




def cryptosellpaymentinfo(request, selling_history_id):
   x = selling_history.objects.get(id=selling_history_id)
   return render(request,'user/dashboard/cryptosellpaymentinfo.html',locals())

def cryptosellconfirm(request, selling_history_id):
   x = selling_history.objects.get(id=selling_history_id)
   s = setup.objects.first()
   ss = s.siteemail
   sid = x.id
   ra = recent_activity.objects.create(user=request.user,name='crypto sell',img=x.coin.logo,amount=x.amount,a_id=sid)
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
   messages.success(request,'crypto transaction is successful wait for the admin approval')
   return redirect('sellinginvoice',selling_history_id=selling_history_id)



def cryptosellcancel(request, selling_history_id):
   user=request.user
   x = selling_history.objects.get(id=selling_history_id)
   x.delete()
   messages.success(request,'transaction cancelled successfully')
   #email sell 
   subject = "Cancelled Transaction"
   message = f""" 
  you have successfully cancelled the sell
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
   return redirect('/cryptobuy')





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



class airtimep(View):
    def get(self, request):
        x = Network.objects.all()
        d = dataplan.objects.all()
        return render(request, 'user/dashboard/airtimep.html',locals())

logger = logging.getLogger(__name__)

class PurchaseView(View):
    def post(self, request):
        user_id = request.user.id  # Get the user ID
        bl = balance.objects.filter(user_id=user_id).first()
        try:
            phone_number = request.POST.get('phone_number')
            network_id = request.POST.get('network_id')
            amount = request.POST.get('amount')

            try:
                product = Network.objects.get(id=network_id)
            except Network.DoesNotExist:
                messages.error(request, 'Product not found')
                return redirect('airtimep')  # Replace with the actual URL name for the airtime page

            if float(amount) > bl.amount:
                messages.error(request, 'Amount is greater than your main balance')
                return redirect('airtimep')  # Replace with the actual URL name for the airtime page
            else:
                api_url = 'https://payvtu.com/api/topup/'
                api_key = settings.AIRTIME_API_KEY

                payload = {
                    'network': network_id,
                    'amount': amount,
                    'mobile_number': phone_number,
                    'Ported_number': True,
                    'airtime_type': 'VTU'
                }
                headers = {
                    'Authorization': f'Token {api_key}',
                    'Content-Type': 'application/json'
                }

                logger.debug(f"Request payload: {payload}")
                response = requests.post(api_url, json=payload, headers=headers)
                response_data = response.json()
                logger.debug(f"Response status code: {response.status_code}")
                logger.debug(f"Response data: {response_data}")

                if response.status_code == 201:
                    transaction_status = response_data.get('Status', 'failed')
                    if transaction_status.lower() == 'successful':
                        bl.amount -= float(amount)
                        bl.save()
                        image_path = static('ui/images/airtime.svg')
                        sv = airtime_Transaction.objects.create(
                            user=request.user,
                            Network=product,
                            amount=amount,
                            number=phone_number,
                            status='successful',
                        )
                        sid = sv.id
                        ra = recent_activity.objects.create(
                        user=request.user,
                        name='airtime purchase',
                        img=image_path,
                        amount=amount,
                        a_id=sid
                        )
                        sv.save()
                        logger.info(f"Transaction successful: {response_data}")
                        messages.success(request, 'Airtime Purchase is successfully')
                        return redirect('activities')  # Replace with the actual URL name for the transaction history page
                    else:
                        logger.error(f"Transaction failed: {response_data}")
                        airtime_Transaction.objects.create(
                            user=request.user,
                            Network=product,
                            amount=amount,
                            number=phone_number,
                            status='failed',
                        )
                        messages.error(request, response_data.get('message', 'Transaction failed'))
                        return redirect('airtimep')  # Replace with the actual URL name for the airtime page
                else:
                    logger.error(f"API error: {response_data}")
                    messages.error(request, response_data.get('message', 'Failed to process transaction'))
                    return redirect('airtimep')  # Replace with the actual URL name for the airtime page
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            messages.error(request, 'Internal server error')
            return redirect('airtimep')  # Replace with the actual URL name for the airtime page




class dataPurchaseView(View):
    def post(self, request):
        user_id = request.user.id  # Get the user ID
        bl = balance.objects.filter(user_id=user_id).first()
        try:
            phone_number = request.POST.get('phone_number')
            network_id = request.POST.get('network_id')

            try:
                product = dataplan.objects.get(id=network_id)
                network_instance = product.Network  # Correctly reference the Network instance
                plan_id = product.plan_id
                price = product.price
            except dataplan.DoesNotExist:
                messages.error(request, 'Product not found')
                return redirect('airtimep')  # Replace with the actual URL name for the data purchase page

            api_url = 'https://payvtu.com/api/data/'
            api_key = settings.AIRTIME_API_KEY

            payload = {
                'network': network_instance.id,
                'mobile_number': phone_number,
                'plan': plan_id,
                'Ported_number': True
            }
            headers = {
                'Authorization': f'Token {api_key}',
                'Content-Type': 'application/json'
            }

            logger.debug(f"Request payload: {payload}")
            response = requests.post(api_url, json=payload, headers=headers)
            response_data = response.json()
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response data: {response_data}")

            if response.status_code == 201:
                transaction_status = response_data.get('Status', 'failed')
                if transaction_status.lower() == 'successful':
                    # Assuming you have a balance deduction logic similar to airtime
                    bl.amount -= float(price)
                    bl.save()

                    airtime_Transaction.objects.create(
                        user=request.user,
                        Network=network_instance,  # Use the Network instance here
                        amount=price,
                        number=phone_number,
                        status='successful',  # Note the correct spelling
                    )

                    logger.info(f"Transaction successful: {response_data}")
                    messages.success(request, 'Transaction completed successfully')
                    return redirect('activities')  # Replace with the actual URL name for the transaction history page
                else:
                    logger.error(f"Transaction failed: {response_data}")
                    messages.error(request, response_data.get('message', 'Transaction failed'))
                    return redirect('airtimep')  # Replace with the actual URL name for the data purchase page
            else:
                logger.error(f"API error: {response_data}")
                messages.error(request, response_data.get('message', 'Failed to process transaction'))
                return redirect('airtimep')  # Replace with the actual URL name for the data purchase page
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            messages.error(request, 'Internal server error')
            return redirect('airtimep') 

def bankhist(request, id):
   x = balance_history.objects.get(pk=id)
   return render(request, 'user/dashboard/bankhist.html',locals())


def autodep(request, id):
   user = request.user
   x = balance_history.objects.get(pk=id)
   user_id = request.user.id
   bl = balance.objects.filter(user_id=user_id).first()
   if x.status == True:
      return redirect('activities')
   else:
    x.status = True
    ba = x.amount
    bl.amount += ba
    bl.save()
    x.save()
    sid = x.id
    image_path = static('ui/images/flutterwave.png')
    ra = recent_activity.objects.create(
                        user=request.user,
                        name='Flutterwave deposit',
                        img=image_path,
                        amount=x.amount,
                        a_id=sid
                        )
    messages.success(request, 'account funded successfully')
   return redirect('activities')

def autodel(request, id):
   x = balance_history.objects.get(pk=id)
   x.delete()
   messages.success(request, 'Deposit cancelled successfully successfully')
   return redirect('activities')

# def forgetpassword(request):
#    return render(request,'user/auth/forgetpassword.html')

def withhis(request, id):
   x = withd_his.objects.get(pk=id)
   return render(request, 'user/dashboard/withhis.html',locals())

#NR6UJ8XXW6LHTERKMZXNGDVF