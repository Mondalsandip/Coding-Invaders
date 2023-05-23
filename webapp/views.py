from django.shortcuts import render
from django.http import HttpResponse
import requests
import base64
import hashlib
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
import qrcode
import os

#newMID = 'TESTMID1UAT'
# newMID = 'UATPROVIDER101'
#txnid = "A2263"

baseUrl = 'https://mercury-uat.phonepe.com'
# MID = 'UATMERCHANT101'
# saltkey = '8289e078-be0b-484d-ae60-052f117f8deb'
# keyindex = '1'


# MID = 'CCDAYUAT'
# saltkey = 'a12acf1d-a14e-41be-90c3-eb0959c9460f'
# keyindex = '1'

# MID = 'RELAXO'
# saltkey = 'c2f4eed5-33fd-1a93-cef3-d58a35a617dc'
# keyindex = '1'

# baseUrl = 'https://mercury-t2.phonepe.com'
# MID = 'APSRTCOFFLINEEPOS'
# saltkey = '0f0a0358-6356-4122-b808-5e352565239d'
# keyindex = '1'

# baseUrl = 'https://mercury-t2.phonepe.com'
# MID = 'IMPRESSIONSYSTEMSNASIK'
# saltkey = 'd96621f5-8b3b-43f0-a20a-c01087b1a6ff'
# keyindex = '1'

# MID = 'PINELABS'
# saltkey = '44b7b096-a48c-43f9-8a60-d74981a52418'
# keyindex = '9'

# MID = 'UATMERCHANT101'
# saltkey = '661efa52-fe56-432e-b7d6-54ef1d0af805' #UATPROVIDER101
# keyindex = '1'

# MID = 'PINELABS'
# saltkey = '8289e078-be0b-484d-ae60-052f117f8deb' #M2401563246873249082352
# keyindex = '1'

# baseUrl ='https://mercury-t2.phonepe.com'
# MID = 'PRODTEST'
# saltkey = '86c3075e-c20f-4516-9628-e9159dcb20cc'
# keyindex = '2'

# baseUrl ='https://mercury-t2.phonepe.com'
# MID = 'DECATHLON'
# saltkey = '465b368f-721e-4228-a467-e5f4cc44ce6e'
# keyindex = '1'

# baseUrl ='https://mercury-t2.phonepe.com'
# MID = 'PRODTEST1'
# saltkey = '4dfb02c9-1f0c-4237-ae02-c5d58a6f2a5f'
# keyindex = '2'

#saltkey ='cde55b48-999d-47e5-b564-68eb12c618fe'  #Genisys
#keyindex='1'
#baseUrl ='https://mercury-t2.phonepe.com'
# MID = 'DAALCHINIUAT'
# saltkey = '7e29b79b-c7c9-49f1-8066-bb8181c78000'
# keyindex = '1'

#txnid='jwgehhdjwe1'
# @api_view(['GET'])
def requestpayment(request):
    url = baseUrl + '/v3/charge'

    payload = {
        "merchantId": MID,
        "transactionId": txnid,
        "merchantOrderId": None,
        "amount": "100",
        "instrumentType": "MOBILE",
        # "subMerchantId":"SM2302231623018321011852",
        #"chargeType" :  "CLOSED_COLLECT",
        #"chargeType": "OPEN_COLLECT",
        #"subMerchantId": "Apollo",
        "instrumentReference": "8798324070",
        # "message":'Hi, this is amit',
        "storeId": "store1",
        # "shortName": "sairamit",
        "terminalId": "terminal1",
        "expiresIn": "180"
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/charge' + saltkey

    str_forSha256 = encodeddata + '/v3/charge' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify)

    headers = {
        "Content-Type": "application/json",
        "x-provider-id": "GINESYSPOS",
        # "x-callback-url": "https://3c07d4cctf.execute-api.ap-northeast-1.amazonaws.com/default/myfunc",
        "x-callback-url":"https://en1rh125epyu9.x.pipedream.net/",
        # "x-call-mode": "POST",
        # "X-REDIRECT-MODE": "POST",
        "X-VERIFY": x_verify
    }
    print(headers)
    print(strjson)
    print(url)
    print(str_forSha256)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(res)
    #
    # print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def canceltransaction(request):
    merchantId = MID
    transactionId = txnid
    url = baseUrl + '/v3/charge/' + merchantId + '/' + transactionId + '/cancel'

    # for Sha256 calculation
    api_saltkey = saltkey

    str_forSha256 = '/v3/charge/' + merchantId + '/' + transactionId + '/cancel' + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }

    print(headers)
    print(url)
    res = requests.post(url=url, headers=headers)
    return HttpResponse(res)
    # return HttpResponse(a)


def checkstatus(request):
    merchantId = MID
    transactionId = txnid
    # transactionId = 'ref_' + txnid
    url = baseUrl + '/v3/transaction/' + merchantId + '/' + transactionId + '/status'

    # for Sha256 calculation
    api_saltkey = saltkey

    str_forSha256 = '/v3/transaction/' + merchantId + '/' + transactionId + '/status' + api_saltkey
    print(str_forSha256)
    print(url)
    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    headers = {
        "Content-Type": "application/json",
        #"x-provider-id": "IMPRESSIONSYSTEMPOS",
        "X-VERIFY": x_verify
    }

    print(x_verify)
    res = requests.get(url=url, headers=headers)
    #return JsonResponse({'a':'b'})
    return HttpResponse(res)


def qrInit(request):
    url = baseUrl + '/v3/qr/init'

    payload = {
        'merchantId': MID,
        'transactionId': txnid,
        "merchantOrderId": "ORDER123",
        'amount': 1000,
        'expiresIn': 180,
        "message": "",
        "subMerchant": "",
        "storeId": "1071296",
        "terminalId": "2190961",
        # "gstBreakup": {},
        # "invoiceDetails": {}
     }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(url)
    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/qr/init' + saltkey

    str_forSha256 = encodeddata + '/v3/qr/init' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "x-callback-url": "https://en1rh125epyu9.x.pipedream.net/",
        # "X-REDIRECT-MODE": "POST",
        # "x-call-mode":"POST",
        #"x-provider-id": "PINELABS",
        "X-VERIFY": x_verify
    }

    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    # print(res.status_code)
    # print(strjson)
    # print(res)
    #
    # print(str_forSha256)
    # print(x_verify)
    # print(res.json()['code'])
    # if res.json()['code'] == 'SUCCESS':
    #     data = res.json()['data']
    #     print('data', data)
    #     img = qrcode.make(data['qrString'])
    #     print('image:', img)
    #     print('type:', type(img))
    #     print('size:', img.size)
    #
    #     ret = HttpResponse(res)
    #     print('image', ret)
    #     # img.save('/Users/amit.aricent/Downloads/qrimage.png')
    #     img.save(os.path.expanduser('~/Downloads/qrimage.png'))
    # else:
    #     ret = HttpResponse(res)
    #return res
    return HttpResponse(res)

def refundpayment(request):
    url = baseUrl + '/v3/credit/backToSource'

    payload = {
        'merchantId': MID,
        'transactionId': 'ref_5' + txnid,
        # 'originalTransactionId': txnid,
        'providerReferenceId':'T2304051036268991328459',
        #'merchantOrderId': 'M123456789',
        'amount': 100,
        #'subMerchantId': 'DemoSubMerchant',
        #'message': 'refund initiated'
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/credit/backToSource' + saltkey

    str_forSha256 = encodeddata + '/v3/credit/backToSource' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify,
        #"x-callback-url": "https://en1ukikex633u.x.pipedream.net/",
        #"x-provider-id": "M2401563246873249082352",
        # "x-call-mode": "POST",
    }

    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(strjson)
    print(url)
    print(str_forSha256)
    print(x_verify)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def remind(request):
    merchantId = MID
    transactionId = txnid
    url = baseUrl + '/v3/charge/' + merchantId + '/' + transactionId + '/remind'

    # for Sha256 calculation
    api_saltkey = saltkey

    str_forSha256 = '/v3/charge/' + merchantId + '/' + transactionId + '/remind' + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }

    print(url)
    print(headers)
    res = requests.post(url=url, headers=headers)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def requestListOfTxn(request):
    url = 'https://mercury-uat.phonepe.com/v3/qr/transaction/list'

    payload = {
        "size": 3,
        "qrCodeId": 'Q323937565',
       # "amount": 100,
       # "last4Digits": "5780"
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/qr/transaction/list' + saltkey

    str_forSha256 = encodeddata + '/v3/qr/transaction/list' + '0a21570f-08fe-4a9f-88e3-8f5924f49e1e'

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify)

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(headers)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(res.json()['code'])
    return HttpResponse(res)


def healthcheckup(request):
    merchantId = MID
    transactionId = txnid
    url = 'https://uptime.phonepe.com/v1/merchants/' + merchantId + '/' + transactionId + '/health'

    # for Sha256 calculation
    api_saltkey = saltkey

    str_forSha256 = '/v1/merchants/' + merchantId + '/' + transactionId + '/health' + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }

    print(headers)
    res = requests.get(url=url, headers=headers)
    return HttpResponse(res)
    # return HttpResponse(a)


def requestv1(request):
    #url = 'https://mercury-uat.phonepe.com/v1/charge'
    url = baseUrl + '/v1/charge'
    payload = {
        'merchantId': MID,
        'transactionId': txnid,
        'merchantOrderId': 'M123456789',
        'amount': 100,
        'mobileNumber': '7065265407',
        'expiresIn': 180,
        'storeId': 'store1',
        'terminalId': 'terminal1'
    }

    # for Sha256 calculation
    str_forSha256 = MID + txnid + '100' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify,
        # "x-call-mode": "POST",
         "x-callback-url": "https://enfmsmfxemkbq.x.pipedream.net/"

    }
    print(headers)
    print('url : ' + url)
    print(payload)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(payload), headers=headers)
    # print(res.status_code)
    # print(res.json()['code'])
    print(res.status_code)
    return HttpResponse(res)
    # return HttpResponse(a)


def checkstatusv1(request):
    merchantId = MID
    transactionId = txnid
    # transactionId = 'ref_' + txnid
    url = baseUrl + '/v1/transaction/' + merchantId + '/' + transactionId + '/status'


    # for Sha256 calculation
    api_saltkey = saltkey

    str_forSha256 = merchantId + transactionId + api_saltkey
    print(url)
    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    # x_verify = sha_value + '###' + keyindex
    x_verify = sha_value

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify,
        "x-salt-index": "1"
    }

    print(headers)
    res = requests.get(url=url, headers=headers)
    return HttpResponse(res)
    # return HttpResponse(a)

def CanORReverse(request):
    url = baseUrl + '/v1/charge/cancelOrReverse'

    payload = {
        'merchantId': MID,
        'transactionId': 'ref_' + txnid,
        'originalTransactionId': txnid,
        'merchantOrderId': 'M123456789',
        'amount': 100
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/charge' + saltkey
    reftxn='ref_' + txnid
    str_forSha256 =MID + reftxn + '100' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(url)
    print(headers)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(payload), headers=headers)
    print(res.status_code)
    print(res)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def Reverse(request):
    url = baseUrl + '/v1/charge/reverse'

    payload = {
        'merchantId': MID,
        'transactionId': 'ref_' + txnid,
        'originalTransactionId': txnid,
        'merchantOrderId': 'M123456789',
        'amount': 100
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/charge' + saltkey
    reftxn='ref_' + txnid
    str_forSha256 =MID + reftxn + '100' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(url)
    print(headers)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(payload), headers=headers)
    print(res.status_code)
    print(res)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)


def ChargeCancelOrReverse(request):
    url = baseUrl + '/v3/charge/cancelOrReverse'

    payload = {
        'merchantId': MID,
        'transactionId': 'ref_' + txnid,
        'originalTransactionId': txnid,
        'merchantOrderId': 'M123456789',
        'amount': 100
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/charge' + saltkey

    str_forSha256 = encodeddata + '/v3/charge/cancelOrReverse' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(headers)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)

    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def requestpaymentv4(request):
    url = baseUrl + '/v4/debit'

    payload = {
        'merchantId': MID,
        'transactionId': txnid,
        'merchantUserId': 'amit090119@gmail.com',
        'amount': 100,
        'mobileNumber': '7065265407',
        'email': 'amit090119@gmail.com'
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    api_saltkey = '/v4/debit' + saltkey

    str_forSha256 = encodeddata + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        # "x-call-mode": "POST",
        "x-callback-url": "https://enzyg9nouj39.x.pipedream.net/",
        # "X-REDIRECT-URL": "",
        # "X-REDIRECT-MODE": "POST",
        "X-VERIFY": x_verify
    }
    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)


def mid_Creation(request):
    url1 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data1 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers1 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    token = res1.json()['token']

    ###################################
    url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v2/profiles'

    data2 = {
        "merchantId": newMID,
        "version": 1,
        "fullName": newMID,
        "displayName": newMID,
        "type": "OFFLINE_ORGANISED",
        "phoneNumber": "1234896789",
        "email": "noreply@noreply.com",
        "mcc": "5311",
        "blacklisted": False,
        "firstPartyMerchant": False,
        "disabled": False,
        "callbackUrl": "",
        "merchantVersion": {
            "merchantId": newMID,
            "version": 1,
            "validFrom": 1568806835000,
            "createdAt": 1568806835000,
            "updatedAt": 1568806835000
        },
        "purposeCode": "00",
        "createdAt": 1568806835930,
        "updatedAt": 1568806835930,
        "attributes": []
    }

    headers2 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    res2 = requests.post(url=url2, data=json.dumps(data2), headers=headers2)

    #############################
    url3 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/security/' + newMID + '/token'

    headers3 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    res3 = requests.post(url=url3, headers=headers3)
    authtoken = res3.json()['token']

    ##############################

    url4 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/config/' + newMID + '/MERCHANT_META'

    headers4 = {
        "Content-Type": "application/json"
    }
    res4 = requests.get(url=url4, headers=headers4)

    ##############################

    url5 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/config/' + newMID

    data5 = {
        "type": "MERCHANT_META",
        "linkEnabled": True,
        "loginModes": [
            "OTP",
            "PASSWORD"
        ],
        "disableAutoLogin": False,
        "jusPayEnabled": True,
        "authorizationToken": "Bearer " + authtoken,
        "rememberMePreference": "INVISIBLE"
    }

    headers5 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    res5 = requests.put(url=url5, data=json.dumps(data5), headers=headers5)

    ##############################

    url6 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/merchants/merchantPspMapping/create'

    data6 = {
        "merchantId": newMID,
        "pspHandle": "ybl",
        "state": "ENABLED"
    }

    headers6 = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + token
    }
    res6 = requests.post(url=url6, data=json.dumps(data6), headers=headers6)
    return HttpResponse(res6)


def set_callback(request):
    url1 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data1 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers1 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    token = res1.json()['token']

    ###############################
    url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v2/profiles'

    data2 = {
        "merchantId": newMID,
        #"providerId": "SWIPEPOSUAT",
        "version": 1,
        "fullName": newMID,
        "displayName": newMID,
        "type": "OFFLINE_ORGANISED",
        "phoneNumber": "1234896789",
        "email": "noreply@noreply.com",
        "mcc": "5311",
        "blacklisted": False,
        "firstPartyMerchant": False,
        "disabled": False,
        #"callbackUrl":"https://payment.netlegends.in/",
        #"callbackUrl":"",
        "merchantVersion": {
            "merchantId": newMID,
            "version": 1,
            "validFrom": 1568806835000,
            "createdAt": 1568806835000,
            "updatedAt": 1568806835000
        },
        "purposeCode": "00",
        "createdAt": 1568806835930,
        "updatedAt": 1568806835930,
        "attributes": []
    }

    headers2 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    res2 = requests.put(url=url2, data=json.dumps(data2), headers=headers2)
    return HttpResponse(res2)


def createSaltKey(request):
    url1 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data1 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers1 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    token = res1.json()['token']

    ###################################
    url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/keys/MERCHANT/' + newMID

    data2 = {
        "count": 1
    }

    headers2 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    res2 = requests.post(url=url2, data=json.dumps(data2), headers=headers2)
    return HttpResponse(res2)


def requestpaymentPaylink(request):
    url =  baseUrl +'/v3/payLink/init'
    # url = 'https://mercury-t2.phonepe.com/v3/payLink/init'

    payload = {
        "merchantId": MID,
        "transactionId": txnid,
        "merchantOrderId": 'M123456789',
        "amount": 100,
        "mobileNumber": "7065265407",
        "message": "collect for 1 order",
        # "email": "amit@gmail.com",
        "expiresIn": 180,
        # "shortName": "DemoCustomer",
        # "subMerchant": "DemoMerchant",
        #"storeId": "storeId1",
        #"terminalId": "terminalId1"
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    api_saltkey = '/v3/payLink/init' + saltkey

    str_forSha256 = encodeddata + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(x_verify)
    print(url)

    headers = {
        "Content-Type": "application/json",
        "x-call-mode": "POST",
        "x-callback-url": "https://enf6bvgmeriel.x.pipedream.net/",
        "X-VERIFY": x_verify
    }
    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)


def collectInteroperable(request):
    url1 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data1 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers1 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    token = res1.json()['token']

    ###################################
    url3 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/security/' + newMID + '/token'

    headers3 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    res3 = requests.post(url=url3, headers=headers3)
    authtoken = res3.json()['token']
    print('authtokenn: '+authtoken)

    ##############################

    url4 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/config/' + newMID + '/MERCHANT_META'

    headers4 = {
        "Content-Type": "application/json"
    }
    res4 = requests.get(url=url4, headers=headers4)
    print(url4)
    print(res4)

    ##############################

    url5 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/config/' + newMID

    data5 = {
        "type": "MERCHANT_META",
        "linkEnabled": True,
        "loginModes": [
            "OTP",
            "PASSWORD"
        ],
        "disableAutoLogin": False,
        "jusPayEnabled": True,
        "authorizationToken": "Bearer " + authtoken,
        "rememberMePreference": "INVISIBLE"
    }

    headers5 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    res5 = requests.put(url=url5, data=json.dumps(data5), headers=headers5)

    url6 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/merchants/merchantPspMapping/create'

    data6 = {
        "merchantId": newMID,
        "pspHandle": "ybl",
        "state": "ENABLED"
    }

    headers6 = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + token
    }
    res6 = requests.post(url=url6, data=json.dumps(data6), headers=headers6)
    return HttpResponse(res5)

    # url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/config/' + newMID
    #
    # data2 = {
    #     "type": "PAYMENT_SOLUTIONS",
    #     "collectConfig": {
    #         "payCompletionBy": 0,
    #         "interOperableCall": False
    #     },
    #     "dynamicQrConfig": {
    #         "payCompletionBy": 0
    #     },
    #     "refundConfig": {
    #         "refundAllowed": False,
    #         "creditLimit": 0,
    #         "expiry": 0
    #     }
    # }
    #
    # headers2 = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer " + token
    # }
    #
    # res2 = requests.put(url=url2, data=json.dumps(data2), headers=headers2)
    # return HttpResponse(res2)

def TransactionListAPI(request):
    #url = 'https://mercury-uat.phonepe.com/v3/qr/transaction/list'
    url = baseUrl + '/v3/qr/transaction/list'
    print(url)
    payload = {
        #PRODTEST QR code : Q792860010
        #UATMERCHANRT101 : Q268568477
        #CCDUAT : Q199640811
        #FKRTTEST : Q321898544
        #KFCDEVYANI :  Q330407793
        #CHARTERED : Q498470410

        "qrCodeId": 'Q792860010',
        "size": 4,
        #"merchantId":MID,
        #"storeId":"111001215",
        # "last4Digits": "3813",
        "amount":100,
        #"startTimestamp":1667923235000
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    api_saltkey = '/v3/qr/transaction/list' + saltkey

    str_forSha256 = encodeddata + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def metaDataAPI(request):
    #url = 'https://mercury-uat.phonepe.com/v3/qr/transaction/list'
    url = baseUrl + '/v1/merchant/transaction/metadata'
    print(url)
    payload = {
        "merchantId": MID,
        "phonepeTransactionId": "T2303031229168608733871",
        "schemaVersionNumber": "CCDV1",
        "metadata": {
            "BILLNUMBER": "bill1234"
        }
    }
    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')
    #encodeddata = 'eyJtZXJjaGFudElkIjoiQ0NEQVlVQVQiLCJwaG9uZXBlVHJhbnNhY3Rpb25JZCI6IlQyMjA4MjYxNTI2MDMzODMzNDY0MzkwIiwic2NoZW1hVmVyc2lvbk51bWJlciI6IkNDRFYxIiwibWV0YWRhdGEiOnsiQklMTE5VTUJFUiI6IjYzNSJ9fQ=='

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))
    #saltkey='a12acf1d-a14e-41be-90c3-eb0959c9460f'

    # for Sha256 calculation
    api_saltkey = '/v1/merchant/transaction/metadata' + saltkey

    str_forSha256 = encodeddata + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(url)
    print(json.dumps(data))
    print(x_verify);
    #print(request)
    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    #print(res.status_code)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    #print(res.json()['code'])
    return HttpResponse(res)
    #return HttpResponse(a)

def ListAppAPI(request):
    #url = 'https://mercury-uat.phonepe.com/v3//transactions/list'
    url = baseUrl + '/v3/transactions/list'

    payload = {
	"merchantId": "UATMERCHANT101",
    "storeId": "store1",
	"size": 50,
	#"start": 32,
	"startTimestamp": 1652463620
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')
    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    api_saltkey = '/v3/transactions/list' + saltkey

    str_forSha256 = encodeddata + api_saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(headers)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(strjson)

    print(str_forSha256)
    print(x_verify)
    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def PG_Pay(request):
    url = 'https://api.phonepe.com/apis/hermes'  /prod
    #url = 'https://api-preprod.phonepe.com/apis/hermes' #UAT
    #url = 'https://api-testing.phonepe.com/apis/hermes' #staging
    url =  url+ '/pg/v1/pay'

    payload = {
   "merchantId": MID,
   "merchantTransactionId": txnid,
   "merchantOrderId": "OD620471739210623",
   "merchantUserId": "MUID123",
   "amount": 100,
   #"redirectUrl": "https://mykewlapp.com/redirect",
   #"redirectMode": "POST",
   #"s2sCallbackUrl": "https://mykewlapp.com/callback",
   #"mobileNumber": "9999999999",
   # "customerDetails": {
   #  "firstName": "Mick",
   #  "lastName": "Schumacher",
   #  "deviceInfo": {
   #     "ipAddress": "10.12.14.16"
   #  }
   # },
   #"productInfo": {},
   "paymentInstrument": {
      "type": "PAY_PAGE"
       #"type": "UPI_QR"

   }
}

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/charge' + saltkey

    str_forSha256 = encodeddata + '/pg/v1/pay' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        # "x-provider-id": "UATPROVIDER101",
        "X-VERIFY": x_verify
    }
    print(headers)
    print(strjson)

    print(str_forSha256)
    print(url)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    #res=None
    print(res.status_code)

    print(res.json()['code'])
    return HttpResponse(res)
    # return HttpResponse(a)

def PG_checkstatus(request):
    merchantId = MID
    transactionId = txnid
    # transactionId = 'ref_' + txnid
    #url = 'https://api-preprod.phonepe.com/apis/hermes' + '/pg/v1/status/' + merchantId + '/' + transactionId
    url = 'https://api.phonepe.com/apis/hermes' + '/pg/v1/status/' + merchantId + '/' + transactionId

    # for Sha256 calculation
    api_saltkey = saltkey

    str_forSha256 = '/pg/v1/status/' + merchantId + '/' + transactionId + api_saltkey
    print(str_forSha256)
    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex
    print(url)
    print(x_verify)
    headers = {
        "Content-Type": "application/json",
        "x-merchant-id": MID,
        "X-VERIFY": x_verify
    }

    print(headers)
    print(txnid)
    print(merchantId)
    res = requests.get(url=url, headers=headers)
    return HttpResponse(res)
    # return HttpResponse(a)


def event(request):
    #url = 'https://api.phonepe.com/apis/hermes'
    #url = 'https://api-preprod.phonepe.com/apis/hermes'
    url = 'https://api-testing.phonepe.com/apis/hermes'
    url =  url+ '/plugin/ingest-event'

    payload = {
   "merchantId": MID,
   "transactionId": 'OD620471739210624',
   "merchantOrderId": "OD620471739210624",
   "merchantUserId": "MUID1234",
   "X-MERCHANT-DOMAIN": "www.amit.com",
   "amount": 100,
   "flowType": "B2B_PG",
    "eventType": "PLUGIN_USER_CANCEL"
   }


    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    # for Sha256 calculation
    # api_saltkey = '/v3/charge' + saltkey

    str_forSha256 = encodeddata + '/plugin/ingest-event' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        # "x-provider-id": "UATPROVIDER101",
        "X-VERIFY": x_verify
    }
    print(headers)
    print(strjson)

    print(str_forSha256)
    print(url)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    #res=None
    print(res.status_code)

    print(res.json()['code'])
    return HttpResponse(res)


def createQRcode(request):
    newMID = 'BYTIZEUAT'
    url1 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/profiles/' + newMID + '/stores/custom'
    data1 = {
        "storeId": "store1",
        "merchantId": newMID,
        "name": newMID,
        "displayName": newMID,
        "address": "test",
        "city": "test",
        "merchantAssignedId": "1030000000000001",
        "active": True,
        "latitude": 0,
        "longitude": 0,
        "attributes": [],
        "createdAt": 1598199114894,
        "updatedAt": 1598199114894,
        "displayState": "PENDING",
        "openTime": -1,
        "closeTime": -1
    }

    headers1 = {
        "Content-Type": "application/json",
    }

    print(headers1)
    print(data1)
    print(url1)
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)

    url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/profiles/' + newMID + '/stores/store1/terminals/custom'
    data2 = {
        "terminalId": "terminal1",
        "storeId": "store1",
        "merchantId": newMID,
        "name": "bdel terminal",
        "active": True,
        "createdAt": 1598201584828,
        "updatedAt": 1598201584828
    }

    headers2 = {
        "Content-Type": "application/json",
    }

    print(headers2)
    print(data2)
    print(url2)
    res2 = requests.post(url=url2, data=json.dumps(data2), headers=headers2)

    url3 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data3 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers3 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res3 = requests.post(url=url3, data=json.dumps(data3), headers=headers3)
    token = res3.json()['token']
    # print(json.dumps(data1))
    # print(url1)
    # print(headers1)
    #token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtZXJjaGFudFNlcnZpY2VfR1UxOTA1MTMxNzAxMDY5OTU3MTM2OTUxIiwiaWF0IjoxNjYxMzQwMDg0LCJpc3MiOiJnYW5kYWxmIiwicm9sZSI6Im1lcmNoYW50U2VydmljZVVzZXIiLCJyb2xlcyI6W10sInR5cGUiOiJkeW5hbWljIiwidmVyc2lvbiI6IjQuMCIsInVzZXJEZXRhaWxzIjp7InVzZXJJZCI6IkdVMTkwNTEzMTcwMTA2OTk1NzEzNjk1MSIsInVzZXJUeXBlIjoiVVNFUiIsIm5hbWUiOiJTaGFzaGFuayBNaXNocmEiLCJlbWFpbCI6InNoYXNoYW5rLm1pc2hyYUBwaG9uZXBlLmNvbSIsInJvbGVJZCI6IlIxOTA3MjIxNTM1MjExNzUxMTA2NzYzIiwicm9sZU5hbWUiOiJzdXBlcmFkbWluIn0sInNpZCI6IjhlOThmMTk1LTI2NGItNDJmNy1iN2FiLTUyZmE3OWQ5Y2JjMSIsInZhbGlkYXRpb25EYXRhIjp7fSwiYXVkIjoibWVyY2hhbnRTZXJ2aWNlIiwic2Vzc2lvbkV4cGlyeSI6MTY2MTM0MzY4NCwidXNlcl9pZCI6Im1lcmNoYW50U2VydmljZV9HVTE5MDUxMzE3MDEwNjk5NTcxMzY5NTEiLCJwZXJtaXNzaW9ucyI6eyJtZXJjaGFudFNlcnZpY2UiOiJ6anRJIiwiZ2FuZGFsZiI6IjczNkJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFDQjRnUUFBQUFBQUFBQUIifSwibmFtZSI6IkdVMTkwNTEzMTcwMTA2OTk1NzEzNjk1MSIsImlkIjoibWVyY2hhbnRTZXJ2aWNlX0dVMTkwNTEzMTcwMTA2OTk1NzEzNjk1MSIsImV4cCI6MTY2MTM0MzY4NH0.cQlSPBPnq7WjcvYe0Jkqyjc7l5EKS5AxvRMzeuKv6f5Hytzinj9J7mhVd0fW6zZy87h1bHuNoO9Eo-lQRjIfgw'

    url4 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/qrcodes/generate/preassigned?psp=ybl'

    data4 = {
        "merchantId": newMID,
        "storeId": "store1",
        "terminalId": "terminal1",
        "mappedMerchantEntity": "TERMINAL"
    }

    headers4 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    print(headers4)
    print(data4)
    print(url4)
    print(token)
    res4 = requests.post(url=url4, data=json.dumps(data4), headers=headers4)
    return HttpResponse(res4)

def updateProvider(request):
    merchantId='UATMERCHANT101'
    providerId='UATPROVIDER101'
    url1 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data1 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers1 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    token = res1.json()['token']

    url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/profiles/'+merchantId+'/provider/'+providerId+'/update'

    headers2 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "X-EndUser-Token":token

    }

    print(headers2)
    print(url2)

    res = requests.patch(url=url2, headers=headers2)
    print(res.status_code)
    return HttpResponse(res.status_code)


def updateCallback(request):
    merchantId='POPSHOEMARTPREPROD'
    callbackurl='https://popularshoemart.org/Test_PhonePae/api/Values/Phonepeint'

    url1 = 'http://gandalf.traefik.uat.phonepe.nb3/v1/auth/login'

    data1 = {
        "type": "SYSTEM",
        "clientId": "merchantService",
        "clientKey": "1234"
    }

    headers1 = {
        "Content-Type": "application/json",
        "namespace": "gandalf"
    }
    res1 = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    token = res1.json()['token']
    print("token:" + token)

    url2 = 'http://merchant-service.traefik.uat.phonepe.nb3/v1/profiles/'+merchantId+'/callbackUrl'

    headers2 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "X-EndUser-Token": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJnYW5kYWxmX0dVMjAwNzEzMTQwNDExODgwOTY1OTQwNCIsImlhdCI6MTY3NDQ2MDY0NywiaXNzIjoiZ2FuZGFsZiIsInJvbGUiOiJnYW5kYWxmVXNlciIsInJvbGVzIjpbXSwidHlwZSI6ImR5bmFtaWMiLCJ2ZXJzaW9uIjoiNC4wIiwidXNlckRldGFpbHMiOnsidXNlcklkIjoiR1UyMDA3MTMxNDA0MTE4ODA5NjU5NDA0IiwidXNlclR5cGUiOiJVU0VSIiwibmFtZSI6IkFtaXQgQXJpY2VudCIsImVtYWlsIjoiYW1pdC5hcmljZW50QHBob25lcGUuY29tIn0sInNpZCI6IjQxYTcyNDRhLWViNzktNDUwNy04OWMyLWY5ZDUzNjliYmU4MSIsInZhbGlkYXRpb25EYXRhIjp7fSwiYXVkIjoiZ2FuZGFsZiIsInNlc3Npb25FeHBpcnkiOjE2NzQ0NjU2NDcsInVzZXJfaWQiOiJnYW5kYWxmX0dVMjAwNzEzMTQwNDExODgwOTY1OTQwNCIsInBlcm1pc3Npb25zIjp7fSwibmFtZSI6IkdVMjAwNzEzMTQwNDExODgwOTY1OTQwNCIsImlkIjoiZ2FuZGFsZl9HVTIwMDcxMzE0MDQxMTg4MDk2NTk0MDQiLCJleHAiOjE2NzQ0NjU2NDd9.Wbkv-Ut2WkAdKscJBnmgMzkRCHiN6cXTCaFvoB7JL5V_WCCeFNmKzABlVIJnDWPEsjeU27E1bMxAibYGFQospA"
    }

    data2 = {
        "callbackUrl": callbackurl
    }

    print(headers2)
    print(url2)

    res = requests.patch(url=url2,data=json.dumps(data2), headers=headers2)
    return HttpResponse(res)


def createSubmerchant(request):
    url = baseUrl + '/v1/submerchant'

    payload = {
        "merchantId": MID,
        "fullName": "submerchant1234",
        "displayName": "submerchant v1",
        "mcc": "5432",
        "aggregatorSubMerchantId": "sub1234",
        "externalMerchantType": "OFFLINE",
        "externalOnboardingType":'AGGREGATORS',
    }

    # for base64 encoded payload
    strjson = json.dumps(payload)
    encoded_dict = strjson.encode('UTF-8')
    encodeddata = base64.b64encode(encoded_dict)
    encodeddata = encodeddata.decode('UTF-8')

    data = {
        "request": encodeddata
    }

    print(json.dumps(data))

    str_forSha256 = encodeddata + '/v1/submerchant' + saltkey

    sha_value = hashlib.sha256(str_forSha256.encode('UTF-8')).hexdigest()

    x_verify = sha_value + '###' + keyindex

    print(x_verify);

    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify
    }
    print(headers)
    print(strjson)
    print(url)
    print(str_forSha256)
    print(x_verify)
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.status_code)
    print(res)
    return HttpResponse(res)



