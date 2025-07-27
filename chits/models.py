from django.db import models
from datetime import date
from django.utils import timezone  


PLAN_CHOICES = (
    ('10000', '₹10,000'),
    ('20000', '₹20,000'),
)

class Member(models.Model):
    name = models.CharField(max_length=100)
    chitti_start_date = models.DateField(default=timezone.now)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    chitti_lifted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.plan}"

class PaymentHistory(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    month = models.DateField(default=date.today)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} - {self.month.strftime('%b %Y')} - {'Paid' if self.is_paid else 'Unpaid'}"
