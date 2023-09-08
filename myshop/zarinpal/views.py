from django.shortcuts import render , get_object_or_404
from orders.models import Order
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from .config import MERCHANT
from orders.tasks import send_order_email
from coupons.models import Coupon
from decimal import Decimal

client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/' # Important: need to edit for realy server.

def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.get_total_cost()
    if request.session.get('coupon_id') != None:
        try:
                coupon =  Coupon.objects.get(id=request.session.get('coupon_id'))
                total_cost_with_discount = total_cost - ((coupon.discount / Decimal(100)) * total_cost)
        except Coupon.DoesNotExist:
                total_cost_with_discount = total_cost
        
        result = client.service.PaymentRequest(MERCHANT, total_cost_with_discount, description, order.email, "mobile", CallbackURL)
    else:
        result = client.service.PaymentRequest(MERCHANT, total_cost, description, order.email, "mobile", CallbackURL) 
            
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order,id=order_id)
        total_cost = order.get_total_cost()
        if request.session.get('coupon_id') != None:
            try:
                coupon =  Coupon.objects.get(id=request.session.get('coupon_id'))
                total_cost_with_discount = total_cost - ((coupon.discount / Decimal(100)) * total_cost)
            except Coupon.DoesNotExist:
                total_cost_with_discount = total_cost
        
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], total_cost_with_discount)
        else:
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], total_cost)
            
        if result.Status == 100:
            order.paid = True
            order.save()
            send_order_email.delay(order.id)
            request.session.pop('coupon_id', None)
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            return render(request,"zarinpal/success.html",{"id":result.RefID})
        elif result.Status == 101:
            # return HttpResponse('Transaction submitted : ' + str(result.Status))
            request.session.pop('coupon_id', None)
            return render(request,"zarinpal/submited.html",{"status":result.Status})
        else:
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
            request.session.pop('coupon_id', None)
            return render(request,"zarinpal/failed.html",{"status":result.Status})
    else:
        # return HttpResponse('Transaction failed or canceled by user')
        request.session.pop('coupon_id', None)    
        return render(request,"zarinpal/cancel.html",{})