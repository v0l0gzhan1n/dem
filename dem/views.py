from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dem.models import CustomUser, Order

from datetime import datetime

def order_view(request):
    today = datetime.now().strftime("%Y-%m-%dT%H:%M")
    if today != datetime.now().strftime("%Y-%m-%dT%H:%M"):
        messages.error(request, "Введите верное время")
    return render(request, 'order/order.html')
# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        full_name = request.POST["full_name"]
        password = request.POST["password1"]
        password2 = request.POST["password2"]
        phone = request.POST["phone"]
        if password == password2:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, phone=phone, full_name=full_name)
            user.save()
            return redirect('/order')
        else:
            messages.error(request, "Пароли не совпадают")
            return redirect('/')
    return render(request, 'users/register.html')

@login_required(login_url='/login')
def order_view(request):
    if request.method == 'POST':
        phone = request.POST["phone"]
        address = request.POST["address"]
        datetime = request.POST["datetime"]
        order_type = request.POST["order_type"]
        payment_type = request.POST["payment_type"]
        other = request.POST.get("other", None)
        comment_others = request.POST.get("comment_others", None)

        if phone and address and datetime and order_type and payment_type is not None:
            if other != 'on':
                order = Order.objects.create(customer=request.user, phone_number=phone, address=address, datetime=datetime, order_type=order_type, payment_type=payment_type,)
                order.save()
                return redirect('/profile')
            else:
                order = Order.objects.create(customer=request.user, phone_number=phone, address=address, datetime=datetime, order_type=order_type, payment_type=payment_type, other=other, comment_others=comment_others)
                order.save()
                return redirect('/profile')
        else:
            messages.error(request, "Заполните все поля")
            return redirect('/order')
    return render(request, 'order/order.html')

@login_required(login_url='/login')
def profile(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'users/profile.html', {'orders': orders})

def logout_view(request):
    logout(request)
    return redirect('/login')