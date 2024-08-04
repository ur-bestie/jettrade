from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
from django.utils import timezone
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
    def __str__(self):
        return self.email
    


class otp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    code1 = models.CharField(max_length=6,default=secrets.token_hex(3))
    verify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    exp = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.user.username
    

class Kycverification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    ID_TYPE_CHOICES = [
        ('Passport', 'Passport'),
        ('National ID', 'National ID'),
        ('Driving License', 'Driving License'),
    ]
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
    id_proof = models.FileField(upload_to='id_proofs/')
    selfie = models.FileField(upload_to='selfies/')
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    status = models.BooleanField(default=False)
    date_summited = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def __str__(self):
         return self.user.username
    

class coins(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='coins/')
    wallet_address = models.CharField(max_length=500, default='hhdudwddjq')
    buying_quantity = models.FloatField(default=0.0,blank=True)
    selling_quantity = models.FloatField(default=0.0,blank=True)

    def __str__(self):
        return self.name
    
    
class setup(models.Model):
    crypto_buying_rate = models.IntegerField(default=0,blank=True)
    crypto_selling_rate = models.IntegerField(default=0,blank=True)
    giftcard_buying_rate = models.IntegerField(default=0,blank=True)
    giftcard_selling_rate = models.IntegerField(default=0,blank=True)
    siteemail = models.CharField(max_length=50,default='Chiagoziewisdom060@gmail.com')


class paymentmethod(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='pmethod/')
    descripton = models.TextField(max_length=3000)
    link = models.URLField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return self.name
    

class buying_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    coin = models.ForeignKey(coins, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(blank=True,default=0)
    rate_naira = models.IntegerField(blank=True,default=0)
    receiving_address = models.CharField(blank=True,max_length=1000)
    payment = models.FloatField(blank=True,default=0.0)
    paymentmethod = models.ForeignKey(paymentmethod, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    invoice = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    buy_date = models.DateTimeField(blank=True,null=True,default=timezone.now)
    def __str__(self):
        return self.user.username
    
class selling_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    coin = models.ForeignKey(coins, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(blank=True,default=0)
    rate_naira = models.IntegerField(blank=True,default=0)
    payment = models.FloatField(blank=True,default=0.0)
    payment_info = models.TextField(max_length=1000)
    status = models.BooleanField(default=False)
    invoice = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sell_date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    
     
    def __str__(self):
        return self.user.username


class giftcards(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='giftcard/')


    def __str__(self):
        return self.name
    

class giftcardbuying_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    giftcard = models.ForeignKey(giftcards, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(blank=True,default=0)
    rate_naira = models.IntegerField(blank=True,default=0)
    recipient_name = models.CharField(blank=True,max_length=1000)
    recipient_whatsapp = models.IntegerField(blank=True,default=0)
    payment = models.FloatField(blank=True,default=0.0)
    paymentmethod = models.ForeignKey(paymentmethod, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    invoice = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    buy_date = models.DateTimeField(blank=True,null=True,default=timezone.now)
    
    def __str__(self):
        return self.user.username
    
class Network(models.Model):
    name = models.CharField(max_length=100)
    pro_id = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.name}"


class airtime_Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    Network = models.ForeignKey(Network, on_delete=models.CASCADE)
    amount = models.IntegerField()
    number = models.IntegerField()
    status = models.CharField(max_length=20)
    transaction_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def __str__(self):
        return self.Network.name
    

class balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.user.username
    

class balance_history(models.Model):
    balance = models.ForeignKey(balance, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

class recent_activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    img = models.FileField(upload_to='ract/')
    amount = models.IntegerField(default=0)
    a_id = models.IntegerField()
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)
     
    def __str__(self):
        return self.name

class dataplan(models.Model):
    Network = models.ForeignKey(Network, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    plan_id = models.IntegerField()
    price = models.IntegerField()
    
    def __str__(self):
        return self.Network.name
    

class datap_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    dataplan = models.ForeignKey(dataplan, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)