from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedCharField, EncryptedDateField, EncryptedIntegerField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = EncryptedDateField()
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    zipCode = models.CharField(max_length = 20)
    SSN = EncryptedCharField(max_length = 15)
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        )
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default= 'pending')
    EMPLOYMENT_CHOICES = (
        ('unemp', 'Unemployed'),
        ('selfemp', 'Self Employed'),
        ('ft', 'Full Time'),
        ('pt', 'Part Time'),
        ('stu', 'Student'),
        )
    employed = models.CharField(max_length = 30, choices = EMPLOYMENT_CHOICES, default = 'unemp')
    employment = models.OneToOneField('Employment', on_delete=models.CASCADE)

class Employment(models.Model):
    employer = models.CharField(max_length = 100, default = "")
    role = models.CharField(max_length = 100)

    #employer address
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    zipCode = models.CharField(max_length = 20)

    #income data
    monthly_income = EncryptedIntegerField(default = 0)
    income_frequency = models.DurationField()
    next_pay_date = EncryptedDateField()






