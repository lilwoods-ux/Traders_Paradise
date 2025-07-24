from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Bot, BotPurchase
import json

OWNER_PASSWORD = "lilwoods72"

def homepage(request):
    return render(request, 'bots/homepage.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('bot_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'bots/login.html')

def user_signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    elif request.method == 'POST':
        messages.error(request, 'Error creating account. Please try again.')
    return render(request, 'bots/signup.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def bot_list(request):
    bots = Bot.objects.all()
    purchased = BotPurchase.objects.filter(user=request.user).values_list('bot_id', flat=True)
    return render(request, 'bots/bot_list.html', {
        'bots': bots,
        'purchased_bot_ids': list(purchased)
    })

@login_required
def upload_bot(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == OWNER_PASSWORD:
            name = request.POST.get('name')
            price = request.POST.get('price')
            file = request.FILES.get('file')
            if name and price and file:
                Bot.objects.create(name=name, price=price, file=file)
                return redirect('bot_list')
            else:
                return render(request, 'bots/upload.html', {'error': 'All fields are required.'})
        else:
            return render(request, 'bots/upload.html', {'error': 'Incorrect password'})
    return render(request, 'bots/upload.html')

@login_required
def delete_bot(request, bot_id):
    bot = get_object_or_404(Bot, id=bot_id)
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == OWNER_PASSWORD:
            bot.delete()
            return redirect('bot_list')
        else:
            return render(request, 'bots/delete.html', {'error': 'Incorrect password', 'bot_id': bot_id})
    return render(request, 'bots/delete.html', {'bot_id': bot_id})

@login_required
def payment(request, bot_id):
    bot = get_object_or_404(Bot, id=bot_id)
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = bot.price
        response = simulate_mpesa_stk_push(phone_number, amount, bot_id)

        if response.get("ResponseCode") == "0":
            BotPurchase.objects.get_or_create(user=request.user, bot=bot)
            return redirect('payment_success', bot_id=bot.id)
        else:
            messages.error(request, "Payment failed. Please try again.")
    return render(request, 'bots/payment.html', {'bot': bot})

@login_required
def payment_success(request, bot_id):
    bot = get_object_or_404(Bot, id=bot_id)
    return render(request, 'bots/payment_success.html', {'bot': bot})

@login_required
def stk_push(request):
    print("stk_push endpoint hit")
    if request.method == 'POST':
        try:
            print("Parsing JSON...")
            data = json.loads(request.body)
            print("Data received:", data)

            bot_id = data.get('bot_id')
            amount = data.get('amount')
            phone = data.get('phone')
            print(f"Bot ID: {bot_id}, Amount: {amount}, Phone: {phone}")

            response = simulate_mpesa_stk_push(phone, amount, bot_id)
            print("Simulated response:", response)

            if response.get("ResponseCode") == "0":
                return JsonResponse({"status": "success", "message": "STK Push sent!"})
            else:
                return JsonResponse({"status": "error", "message": "Payment failed"})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=400)

    print("Invalid method")
    return JsonResponse({"error": "Invalid request method"}, status=405)

def simulate_mpesa_stk_push(phone, amount, bot_id):
    # This is just a simulation. You can replace this with the actual Safaricom API.
    return {
        "ResponseCode": "0",
        "CustomerMessage": "Success",
        "MerchantRequestID": "123456",
        "CheckoutRequestID": "ABCDEF"
    }

def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')
