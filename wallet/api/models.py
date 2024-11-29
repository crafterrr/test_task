from django.db import models, transaction


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['label']),
            models.Index(fields=['balance']),
        ]


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['txid']),
            models.Index(fields=['wallet']),
            models.Index(fields=['amount']),
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.wallet.balance += self.amount
            if self.wallet.balance < 0:
                raise ValueError("Wallet balance cannot be negative")
            super().save(*args, **kwargs)
            self.wallet.save()
