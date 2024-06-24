from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import uuid

class Membership(models.Model):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    MEMBERSHIP_PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Advance', 'Advance'),
        ('Pro', 'Pro')
    ]
    membership_plan = models.CharField(max_length=100, choices=MEMBERSHIP_PLAN_CHOICES)
    tenure = models.PositiveIntegerField(choices=[(3, '3 months'), (6, '6 months'), (12, '12 months')])
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending')
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = datetime.now().date()

        if not self.end_date:
            if self.tenure == 3:
                self.end_date = self.start_date + timedelta(days=90)
            elif self.tenure == 6:
                self.end_date = self.start_date + timedelta(days=180)
            elif self.tenure == 12:
                self.end_date = self.start_date + timedelta(days=365)

        super().save(*args, **kwargs)

class Member(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    membership_plan = models.CharField(max_length=100)
    unique_number = models.IntegerField(unique=True)
    tenure = models.PositiveIntegerField(default=0)
    start_date = models.DateField(default=timezone.now)  # Set default value to current date
    end_date = models.DateField(default=timezone.now)

    class Meta:
        app_label = 'gym'

class Attendance(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} - {self.entry_time}"
