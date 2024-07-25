from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('userkyc',views.userkyc,name='userkyc'),
    path('keycreject/<str:id>',views.keycreject,name='keycreject'),
    path('userkycview/<str:id>',views.userkycview,name='userkycview'),
    path('trancryptobuy',views.trancryptobuy,name='trancryptobuy'),
    path('trancryptosell',views.trancryptosell,name='trancryptosell'),
    path('trangiftbuy',views.trangiftbuy,name='trangiftbuy'),
    path('trancryptobuydelete/<str:id>',views.trancryptobuydelete,name='trancryptobuydelete'),
    path('trancryptoselldelete/<str:id>',views.trancryptoselldelete,name='trancryptoselldelete'),
    path('trangiftbuydelete/<str:id>',views.trangiftbuydelete,name='trangiftbuydelete'),
    path('cryptoproduct',views.cryptoproduct,name='cryptoproduct'),
    path('giftcardproduct',views.giftcardproduct,name='giftcardproduct'),
    path('cryptoproductdel/<str:id>',views.cryptoproductdel,name='cryptoproductdel'),
    path('cryptoproductedit/<str:id>',views.cryptoproductedit,name='cryptoproductedit'),
    path('giftcardproductdel/<str:id>',views.giftcardproductdel,name='giftcardproductdel'),
    path('giftcardproductedit/<str:id>',views.giftcardproductedit,name='giftcardproductedit'),
    path('passwordchange',views.passwordchange,name='passwordchange'),
    path('adminsettings',views.adminsettings,name='adminsettings'),
    path('deposit',views.deposit,name='deposit'),

]