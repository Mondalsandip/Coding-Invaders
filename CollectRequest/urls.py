"""CollectRequest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import requestpayment,canceltransaction,checkstatus,refundpayment,qrInit,healthcheckup,collectInteroperable,requestListOfTxn,PG_Pay, PG_checkstatus,event,metaDataAPI,remind,createQRcode,updateCallback
from webapp.views import requestpaymentv4,requestv1,checkstatusv1,ChargeCancelOrReverse,mid_Creation,set_callback,createSaltKey,requestpaymentPaylink,TransactionListAPI,ListAppAPI,Reverse,CanORReverse,updateProvider,createSubmerchant

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request/',requestpayment),
    path('cancel/',canceltransaction),
    path('status/',checkstatus),
    path('refund/',refundpayment),
    path('qr/',qrInit),
    path('remind/',remind),
    path('list/',requestListOfTxn),
    path('health/',healthcheckup),
    path('requestv1/',requestv1),
    path('statusv1/',checkstatusv1),
    path('cancelrev/', ChargeCancelOrReverse),
    path('reverse/', Reverse),
    path('CanORReverse/', CanORReverse),
    path('requestv4/',requestpaymentv4),
    path('createmid/',mid_Creation),
    path('setcallback/',set_callback),
    path('createKey/',createSaltKey),
    path('requestPay/',requestpaymentPaylink),
    path('interoperate/',collectInteroperable),
    path('txnlist/',TransactionListAPI),
    path('metadata/',metaDataAPI),
    path('listapi/', ListAppAPI),
    path('pgpay/',PG_Pay),
    path('pgstatus/',PG_checkstatus),
    path('event/',event,name='e'),
    path('createqr/',createQRcode,name='e'),
    path('updateprovider/',updateProvider),
    path('updatecallback/',updateCallback),
    path('createsubmerchant/',createSubmerchant),
]
