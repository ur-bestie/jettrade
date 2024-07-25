from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import airtimep,PurchaseView,dataPurchaseView
urlpatterns = [
    path('',views.index,name='index'),
    path('user',views.userdash,name='user'),
    path('register',views.register,name='register'),
    path('login', views.user_login,name='login'),
    path('addfunds',views.addfunds,name='addfunds'),
    path('bankfunds',views.bankfunds,name='bankfunds'),
    path('confirmbankdeposit',views.confirmbankdeposit,name='confirmbankdeposit'),
    path('emailverification/<str:username>',views.emailverification,name='emailverification'),
    path('bankhist/<str:id>',views.bankhist,name='bankhist'),
    path('giftcard',views.giftcard,name='giftcard'),
    path('cryptobuy',views.cryptobuy,name='cryptobuy'),
    path('passreset',views.passreset,name='passreset'),
    path('resend_otp',views.resend_otp,name='resend_otp'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('kyc',views.kyc,name='kyc'),
    path('cryptosell',views.cryptosell,name='cryptosell'),
    path('sellinginvoice/<int:selling_history_id>/',views.sellinginvoice,name='sellinginvoice'),
    path('selling_history',views.selling_hist,name='selling_history'),
    path('buyinginvoice/<int:buying_history_id>/',views.buyinginvoice,name='buyinginvoice'),
    path('buying_history',views.buying_hist,name='buying_history'),
    path('activities',views.activities,name='activities'),
    path('giftcardbuy',views.giftcardbuy,name='giftcardbuy'),
    path('giftcardbuyinginvoice/<int:buying_history_id>/',views.giftcardbuyinginvoice,name='giftcardbuyinginvoice'),
    path('giftcardbuying_hist',views.giftcardbuying_hist,name='giftcardbuying_hist'),
    path('paymentinfo/<str:buying_history_id>',views.paymentinfo,name='paymentinfo'),
    path('cryptobuyconfirm/<str:buying_history_id>',views.cryptobuyconfirm,name='cryptobuyconfirm'),
    path('cryptobuycancel/<str:buying_history_id>',views.cryptobuycancel,name='cryptobuycancel'),
 
    path('cryptosellpaymentinfo/<str:selling_history_id>',views.cryptosellpaymentinfo,name='cryptosellpaymentinfo'),
    path('cryptosellconfirm/<str:selling_history_id>',views.cryptosellconfirm,name='cryptosellconfirm'),
    path('cryptosellcancel/<str:selling_history_id>',views.cryptosellcancel,name='cryptosellcancel'),

    path('giftcardbuypaymentinfo/<str:buying_history_id>',views.giftcardbuypaymentinfo,name='giftcardbuypaymentinfo'),
    path('giftcardbuyconfirm/<str:buying_history_id>',views.giftcardbuyconfirm,name='giftcardbuyconfirm'),
    path('giftcardbuycancel/<str:buying_history_id>',views.giftcardbuycancel,name='giftcardbuycancel'),
    path('airtimep',airtimep.as_view(), name='airtimep'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('dataPurchase/', dataPurchaseView.as_view(), name='dataPurchase'),


    path('forgetpassword/',auth_views.PasswordResetView.as_view(),name='forgetpassword'),
    path('password_reset_done',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('forgetpasswordconfirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='forgetpasswordconfirm'),
    path('forgetpasswordcomplete',auth_views.PasswordResetCompleteView.as_view(),name='forgetpasswordcomplete'),
]