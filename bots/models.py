from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    file = models.FileField(upload_to='bots/')  # Files will be stored in media/bots/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class BotPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot = models.ForeignKey('Bot', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bot.name}"
