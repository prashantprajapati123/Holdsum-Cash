from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedCharField, EncryptedDateField
from localflavor.us.models import USStateField, USZipCodeField

from .fields import EncryptedSSNField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = EncryptedDateField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = USStateField()
    zipCode = USZipCodeField()
    SSN = EncryptedSSNField()
    plaid_public_token = EncryptedCharField(max_length=200, blank=True)
    plaid_access_token = EncryptedCharField(max_length=200, blank=True)
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    EMPLOYMENT_CHOICES = (
        ('unemp', 'Unemployed'),
        ('selfemp', 'Self Employed'),
        ('ft', 'Full Time'),
        ('pt', 'Part Time'),
        ('stu', 'Student'),
    )
    employed = models.CharField(max_length=30, choices=EMPLOYMENT_CHOICES, default='unemp')

    def __str__(self):
        return '{user.first_name}, {user.last_name}'.format(user=self.user)
