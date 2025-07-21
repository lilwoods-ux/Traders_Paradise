from django.http import JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Bot
from django.contrib.auth.decorators import login_required


OWNER_PASSWORD = "lilwoods72"  # Match this with upload password

@login_required
def upload_bot(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == OWNER_PASSWORD:
            name = request.POST['name']
            price = request.POST['price']
            file = request.FILES['file']
            Bot.objects.create(name=name, price=price, file=file)
            return redirect('bot_list')
        else:
            return render(request, 'bots/upload.html', {'error': 'Incorrect password'})
    return render(request, 'bots/upload.html')

@login_required
def delete_bot(request, bot_id):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == OWNER_PASSWORD:
            bot = Bot.objects.get(id=bot_id)
            bot.delete()
            return redirect('bot_list')
        else:
            return render(request, 'bots/delete.html', {'error': 'Incorrect password', 'bot_id': bot_id})
    return render(request, 'bots/delete.html', {'bot_id': bot_id})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def bot_list(request):
    bots = Bot.objects.all()
    # Simplified for now: Assume purchased if user is logged in (replace with real logic later)
    bot_purchased = {bot.id: False for bot in bots}  # Initialize all as not purchased
    # Add real purchase check here (e.g., query a Purchase model)
    return render(request, 'bots/index.html', {'bots': bots, 'bot_purchased': bot_purchased})

@login_required
def stk_push(request):
    if request.method == 'POST':
        data = request.json()
        bot_id = data.get('bot_id')
        amount = data.get('amount')
        bot = Bot.objects.get(id=bot_id)
        # Simulate M-Pesa STK push (replace with real API call)
        access_token = "dummy_token"  # Replace with get_mpesa_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": "your_shortcode",
            "Password": "your_password",  # Replace with generate_mpesa_password()
            "Timestamp": "202507190225",  # Replace with get_timestamp()
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": "2547XXXXXXXX",  # Replace with user's phone
            "PartyB": "your_shortcode",
            "PhoneNumber": "2547XXXXXXXX",  # Replace with user's phone
            "CallBackURL": "https://yourdomain.com/callback",
            "AccountReference": f"Bot_{bot_id}",
            "TransactionDesc": "Purchase of Trading Bot"
        }
        # Placeholder response (replace with real requests.post)
        response = {"ResponseCode": "0", "CustomerMessage": "Success"}
        if response.get("ResponseCode") == "0":
            # Mark as purchased (simulated for now)
            # In reality, update this after callback confirmation
            return JsonResponse({"status": "success", "message": "Payment initiated"})
        return JsonResponse({"status": "error", "message": "Payment failed"})
    return JsonResponse({"error": "Invalid request"}, status=400)
def get_mpesa_access_token():
    # Implement M-Pesa OAuth token retrieval
    pass

def generate_mpesa_password():
    # Implement M-Pesa password generation
    pass

def get_timestamp():
    # Implement timestamp generation
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d%H%M%S')
